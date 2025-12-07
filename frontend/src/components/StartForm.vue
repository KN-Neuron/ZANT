<script setup>
import { ref, watch, computed } from 'vue'
import { store } from '@/stores/step.js'
import { useFormStore } from '@/stores/form.js'
import Robot from './Robot.vue'

const formStore = useFormStore()

// Domyślna selekcja
if (store.selectedForms.length === 0) {
    store.selectedForms = ['Accident']
}

// Stany AI
const aiState = ref('idle')
const aiMessage = ref('')
const userResponse = ref('')
const isDownloading = ref(false)
const showDeathAlert = ref(false) // Flaga dla aktu zgonu

// Watcher walidacji
watch(() => store.triggerValidation, (newVal) => {
  if (newVal === true) {
    store.step = 3
    runAnalysis()
    store.triggerValidation = false
  }
})

// --- NAWIGACJA ---

function startProcess() {
    if (store.selectedForms.length === 0) {
        alert("Proszę wybrać przynajmniej jeden formularz.")
        return
    }
    if (store.selectedForms.includes('Accident')) {
        store.step = 1
    } else {
        store.step = 2
    }
}

function goBack() {
    if (store.step === 2 && store.selectedForms.includes('Accident')) {
        store.step = 1
    } else if (store.step === 3) {
        store.step = store.selectedForms.includes('Victim') ? 2 : 1
    } else {
        store.step = -1
    }
}

function goNext() {
    if (store.step === 1 && store.selectedForms.includes('Victim')) {
        store.step = 2
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }
    else {
        store.step = 3
        runAnalysis()
    }
}

function skipAnalysis() {
    store.step = 4
}

// Teksty UI
const stepTitle = computed(() => {
    if (store.step === 1) return 'Krok 1: Zawiadomienie o wypadku'
    if (store.step === 2) return 'Krok 2: Wyjaśnienia poszkodowanego'
    return ''
})

const stepDescription = computed(() => {
    if (store.step === 1) return 'Wypełnij cały formularz zawiadomienia o wypadku (wszystkie sekcje).'
    if (store.step === 2) return 'Wypełnij formularz wyjaśnień poszkodowanego.'
    return ''
})

// --- LOGIKA AI ---

async function runAnalysis() {
  aiState.value = 'analyzing'
  aiMessage.value = "Asystent analizuje Twój opis pod kątem 4 ustawowych przesłanek wypadku..."
  showDeathAlert.value = false // Reset flagi

  try {
    let desc = formStore.data.accident.circumstances || ""
    const injuries = (formStore.data.accident.injuries || "").toLowerCase()

    // SPRAWDZANIE CZY WYSTĄPIŁ ZGON
    if (injuries.includes('zgon') || injuries.includes('śmierć') || injuries.includes('śmierteln')) {
        showDeathAlert.value = true
    }

    if (store.selectedForms.includes('Victim') && formStore.data.description?.text) {
        desc += " [WYJAŚNIENIA POSZKODOWANEGO]: " + formStore.data.description.text
    }

    const payload = {
        accident: {
            circumstances: desc,
            injuries: formStore.data.accident.injuries || ""
        }
    }

    const response = await fetch('/raport-wypadku/api/validate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })

    if (!response.ok) throw new Error("Błąd sieci")
    const result = await response.json()

    await new Promise(r => setTimeout(r, 1000))

    if (result.is_complete) {
        aiState.value = 'success'
        aiMessage.value = "Świetnie! Twój opis jest kompletny i zawiera wszystkie elementy wymagane przez ZUS."
    } else {
        aiState.value = 'questioning'
        aiMessage.value = result.feedback
    }

  } catch (e) {
      console.error(e)
      aiState.value = 'questioning'
      aiMessage.value = "Mam trudność ze zrozumieniem przyczyny zewnętrznej. Czy w zdarzeniu brała udział maszyna, śliska nawierzchnia lub inny czynnik spoza Twojego organizmu?"
  }
}

function submitUserResponse() {
    if(!userResponse.value) return;
    formStore.data.accident.circumstances += ` (Dodatkowe wyjaśnienie: ${userResponse.value})`
    userResponse.value = ''
    runAnalysis()
}

// --- LOGIKA POBIERANIA PDF ---

async function downloadPDF(docType) {
    if (isDownloading.value) return
    isDownloading.value = true

    try {
        const pdfPayload = {
            platnik_nazwa: formStore.data.notifier.businessName || "Brak nazwy",
            platnik_adres: `${formStore.data.notifier.address.street} ${formStore.data.notifier.address.houseNumber}`,
            platnik_nip: formStore.data.notifier.nip || "",
            platnik_dowod_rodzaj: formStore.data.notifier.documentType || "",
            platnik_dowod_numer: formStore.data.notifier.documentNumber || "",

            poszkodowany_nazwa: `${formStore.data.victim.firstName} ${formStore.data.victim.lastName}`.trim(),
            poszkodowany_pesel: formStore.data.victim.pesel || "",
            poszkodowany_dowod_rodzaj: formStore.data.victim.documentType || "",
            poszkodowany_dowod_numer: formStore.data.victim.documentNumber || "",
            poszkodowany_adres: `${formStore.data.victim.address.street} ${formStore.data.victim.address.houseNumber}`,
            tytul_ubezpieczenia: formStore.data.notifier.pkdCode || "Działalność gospodarcza",

            wypadek_zgloszenie: new Date().toLocaleDateString('pl-PL'),
            wypadek_okolicznosci: formStore.data.accident.circumstances || "",
            wypadek_przyczyna_bezp: formStore.data.accident.injuries || "Nie podano",
            wypadek_przyczyna_posr: "---",

            swiadek_1: formStore.data.witnesses?.[0]?.lastName ? `${formStore.data.witnesses[0].firstName} ${formStore.data.witnesses[0].lastName}` : "-",
            swiadek_2: "-"
        }

        const response = await fetch('/raport-wypadku/api/generate-pdf/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pdfPayload)
        })

        if (!response.ok) throw new Error('Błąd generowania PDF po stronie serwera')

        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        const suffix = docType === 'Accident' ? 'Zawiadomienie' : 'Wyjasnienia'
        link.download = `ZUS_${suffix}_${formStore.data.notifier.nip || 'Draft'}.pdf`

        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)

    } catch (e) {
        console.error(e)
        alert("Wystąpił błąd podczas generowania pliku: " + e.message)
    } finally {
        isDownloading.value = false
    }
}
</script>

<template>
  <div class="flex flex-col items-center gap-6 p-4 w-full">

    <!-- Progress Bar -->
    <div class="flex flex-row items-center justify-center gap-4 w-full max-w-lg mb-4">
        <div v-for="i in 4" :key="i" class="flex items-center">
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm transition-colors duration-300"
                 :class="store.step >= i ? 'bg-[#006B34] text-white' : 'bg-gray-200 text-gray-500'">
                 {{ i === 4 ? '⬇' : i }}
            </div>
            <div v-if="i < 4" class="w-8 h-1 transition-colors duration-300" :class="store.step > i ? 'bg-[#006B34]' : 'bg-gray-200'"></div>
        </div>
    </div>

    <div class="flex flex-row w-full bg-white rounded-2xl p-6 shadow-xl min-h-[450px]">

      <!-- Robot Avatar (Lewa strona) -->
      <div class="hidden md:flex flex-col items-center pr-8 border-r border-gray-100 min-w-[200px]">
        <Robot />
        <p class="mt-4 font-bold text-[#006B34]">ZANT Asystent</p>
      </div>

      <!-- Treść (Prawa strona) -->
      <div class="flex flex-col flex-1 pl-0 md:pl-8 justify-center relative">

        <!-- KROK -1: Wybór -->
        <div v-if="store.step === -1" class="animate-in fade-in duration-500">
             <h1 class="text-3xl font-extrabold text-gray-800 mb-4">Dzień dobry!</h1>
             <p class="text-lg text-gray-600 mb-6">Wybierz dokumenty, które chcesz dzisiaj wypełnić.</p>

             <div class="flex flex-col gap-4 mb-8">
                 <label class="flex items-center p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                        :class="store.selectedForms.includes('Accident') ? 'border-[#006B34] bg-green-50' : 'border-gray-200'">
                     <input type="checkbox" value="Accident" v-model="store.selectedForms" class="w-5 h-5 text-[#006B34] rounded focus:ring-[#006B34]">
                     <div class="ml-3">
                         <span class="block font-bold text-gray-800">Zawiadomienie o wypadku (ZUS EWYP)</span>
                         <span class="text-sm text-gray-500">Główny formularz zgłoszeniowy</span>
                     </div>
                 </label>

                 <label class="flex items-center p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                        :class="store.selectedForms.includes('Victim') ? 'border-[#006B34] bg-green-50' : 'border-gray-200'">
                     <input type="checkbox" value="Victim" v-model="store.selectedForms" class="w-5 h-5 text-[#006B34] rounded focus:ring-[#006B34]">
                     <div class="ml-3">
                         <span class="block font-bold text-gray-800">Wyjaśnienia poszkodowanego</span>
                         <span class="text-sm text-gray-500">Protokół wyjaśnień (Opcjonalny)</span>
                     </div>
                 </label>
             </div>

             <button @click="startProcess" class="self-start px-8 py-3 bg-[#006B34] text-white rounded-lg font-bold hover:bg-green-700 shadow-md">
                 Rozpocznij wypełnianie
             </button>
        </div>

        <!-- KROK 1 lub 2: Interfejs z nawigacją -->
        <div v-if="store.step === 1 || store.step === 2" class="animate-in slide-in-from-right-8 duration-500 flex flex-col h-full">
            <div class="flex-1">
                <h2 class="text-2xl font-bold text-gray-800 mb-3">{{ stepTitle }}</h2>
                <p class="text-lg text-gray-600 leading-relaxed">
                    {{ stepDescription }}
                </p>
                <div v-if="store.step === 1 && store.selectedForms.includes('Victim')" class="mt-4 text-blue-600 bg-blue-50 p-3 rounded">
                    ℹ️ Po wypełnieniu tego formularza automatycznie przejdziemy do Wyjaśnień Poszkodowanego.
                </div>
            </div>

            <div class="mt-8 flex justify-between border-t pt-4">
                <button @click="goBack" class="px-4 py-2 text-gray-600 font-medium hover:text-black hover:bg-gray-100 rounded">
                    ← Wróć
                </button>

                <div class="flex gap-3">
                    <button @click="skipAnalysis" class="px-4 py-2 text-gray-500 font-medium hover:text-red-600 hover:bg-red-50 rounded border border-transparent hover:border-red-100">
                        Pomiń weryfikację i pobierz
                    </button>

                    <button @click="goNext" class="px-6 py-2 bg-blue-600 text-white font-bold rounded hover:bg-blue-700 shadow flex items-center gap-2">
                        {{ (store.step === 1 && store.selectedForms.includes('Victim')) ? 'Zapisz i przejdź do Wyjaśnień' : 'Zakończ i sprawdź z Asystentem' }}
                        <span>→</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- KROK 3: AI Konsultant -->
        <div v-if="store.step === 3" class="flex flex-col h-full justify-center relative">
             <div class="absolute top-0 right-0">
                <button @click="skipAnalysis" class="text-xs text-gray-400 hover:text-red-500 underline p-2">
                    Pomiń
                </button>
            </div>

            <div v-if="aiState === 'analyzing'" class="flex flex-col items-center justify-center py-10">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#006B34] mb-4"></div>
                <p class="text-lg font-medium text-gray-600">{{ aiMessage }}</p>
            </div>

            <div v-if="aiState === 'questioning'" class="animate-in fade-in slide-in-from-bottom-4 duration-500">
                <h2 class="text-xl font-bold text-orange-600 mb-4">Asystent ma pytanie:</h2>

                <div class="bg-orange-50 p-5 rounded-xl rounded-tl-none border border-orange-200 mb-6 relative shadow-sm">
                    <p class="text-gray-800 font-medium text-lg italic">"{{ aiMessage }}"</p>
                </div>

                <div class="flex gap-2">
                    <input v-model="userResponse" @keyup.enter="submitUserResponse" type="text" placeholder="Wpisz odpowiedź..."
                           class="flex-1 border border-gray-300 rounded-lg p-3 outline-none">
                    <button @click="submitUserResponse" class="px-6 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 font-semibold shadow-md">
                        Wyślij
                    </button>
                </div>
                 <div class="mt-4 text-center">
                    <button @click="skipAnalysis" class="text-gray-500 text-sm hover:underline">
                        Nie chcę odpowiadać, wygeneruj dokumenty
                    </button>
                </div>
            </div>

            <div v-if="aiState === 'success'" class="animate-in zoom-in duration-300">
                <h2 class="text-2xl font-bold text-[#006B34] mb-2">Analiza zakończona pomyślnie!</h2>
                <p class="text-gray-600 mb-6">{{ aiMessage }}</p>

                <div class="grid grid-cols-2 gap-4 mb-8">
                    <div class="p-2 bg-gray-50 rounded border text-green-700 font-medium">✅ Nagłość</div>
                    <div class="p-2 bg-gray-50 rounded border text-green-700 font-medium">✅ Przyczyna Zewn.</div>
                    <div class="p-2 bg-gray-50 rounded border text-green-700 font-medium">✅ Uraz</div>
                    <div class="p-2 bg-gray-50 rounded border text-green-700 font-medium">✅ Związek z pracą</div>
                </div>

                <!-- ALERT O ZGONIE -->
                <div v-if="showDeathAlert" class="mb-8 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 animate-pulse">
                    <p class="font-bold text-lg">⚠️ Uwaga: Wypadek śmiertelny</p>
                    <p>Z uwagi na wskazany skutek (zgon), <strong>koniecznie dołącz Akt Zgonu</strong> do składanej dokumentacji.</p>
                </div>

                <div class="flex gap-4">
                     <button @click="store.step = 1" class="px-4 py-3 text-gray-600 border rounded hover:bg-gray-50">
                        Edytuj dane
                    </button>
                    <button @click="store.step = 4" class="flex-1 py-3 bg-[#006B34] text-white rounded-lg font-bold hover:bg-green-700 shadow-lg text-lg">
                        Przejdź do pobierania
                    </button>
                </div>
            </div>
        </div>

        <!-- KROK 4: Pobieranie -->
        <div v-if="store.step === 4" class="animate-in fade-in duration-500">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Gotowe!</h2>
            <p class="mb-6 text-gray-600">Oto Twoje dokumenty. Możesz je pobrać.</p>

            <div class="space-y-4">
                <div v-if="store.selectedForms.includes('Accident')"
                     class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer group transition-colors"
                     @click="downloadPDF('Accident')">
                    <div class="flex items-center gap-4">
                        <div class="bg-red-100 text-red-600 p-3 rounded-lg font-bold">PDF</div>
                        <div>
                            <p class="font-bold text-gray-800 text-lg">Zawiadomienie o wypadku</p>
                            <p class="text-sm text-gray-500">Wypełniony formularz zgłoszeniowy</p>
                        </div>
                    </div>
                    <button class="text-[#006B34] font-bold group-hover:underline text-lg">
                        {{ isDownloading ? 'Generowanie...' : 'Pobierz ⬇' }}
                    </button>
                </div>

                <div v-if="store.selectedForms.includes('Victim')"
                     class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer group transition-colors"
                     @click="downloadPDF('Victim')">
                    <div class="flex items-center gap-4">
                        <div class="bg-red-100 text-red-600 p-3 rounded-lg font-bold">PDF</div>
                        <div>
                            <p class="font-bold text-gray-800 text-lg">Wyjaśnienia poszkodowanego</p>
                            <p class="text-sm text-gray-500">Protokół wyjaśnień</p>
                        </div>
                    </div>
                    <button class="text-[#006B34] font-bold group-hover:underline text-lg">
                         {{ isDownloading ? 'Generowanie...' : 'Pobierz ⬇' }}
                    </button>
                </div>
            </div>

            <div class="mt-10 pt-6 border-t text-center">
                <button @click="store.step = -1; store.selectedForms = []" class="text-gray-500 hover:text-black hover:underline text-sm">
                    Rozpocznij nowe zgłoszenie
                </button>
            </div>
        </div>

      </div>
    </div>
  </div>
</template>