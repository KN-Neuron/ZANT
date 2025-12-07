<script setup>
import { ref, watch } from 'vue'
import { store } from '@/stores/step.js'
import { useFormStore } from '@/stores/form.js'
import Robot from './Robot.vue'

const formStore = useFormStore()

// Stany AI Asystenta
const aiState = ref('idle') // 'idle', 'analyzing', 'questioning', 'success'
const aiMessage = ref('')
const userResponse = ref('')

// Watcher: Reaguje na przycisk "Zakończ i sprawdź" z formularza
watch(() => store.triggerValidation, (newVal) => {
  if (newVal === true) {
    store.step = 3
    runAnalysis()
    store.triggerValidation = false
  }
})

// Logika Asystenta (Pytania i Walidacja)
async function runAnalysis() {
  aiState.value = 'analyzing'
  aiMessage.value = "Asystent analizuje Twój opis pod kątem 4 ustawowych przesłanek wypadku (nagłość, przyczyna zewnętrzna...)"

  try {
    const payload = {
        // Przekazujemy dane z formularza do backendu
        accident: {
            circumstances: formStore.data.accident.circumstances || "",
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

    // Symulujemy "myślenie" robota (UX)
    await new Promise(r => setTimeout(r, 1500))

    if (result.is_complete) {
        aiState.value = 'success'
        aiMessage.value = "Świetnie! Twój opis jest kompletny i zawiera wszystkie elementy wymagane przez ZUS. Możemy generować dokumenty."
    } else {
        aiState.value = 'questioning'
        aiMessage.value = result.feedback // To jest pytanie wygenerowane przez AI w backendzie
    }

  } catch (e) {
      console.error(e)
      // Fallback w razie błędu API
      aiState.value = 'questioning'
      aiMessage.value = "Mam trudność ze zrozumieniem przyczyny zewnętrznej. Czy w zdarzeniu brała udział maszyna, śliska nawierzchnia lub inny czynnik spoza Twojego organizmu?"
  }
}

// Obsługa odpowiedzi użytkownika na pytanie AI
function submitUserResponse() {
    if(!userResponse.value) return;

    // Doklejamy odpowiedź do głównego opisu w formularzu
    formStore.data.accident.circumstances += ` (Dodatkowe wyjaśnienie poszkodowanego: ${userResponse.value})`
    userResponse.value = ''

    // Ponowna analiza
    runAnalysis()
}

function finishProcess() {
    store.step = 4 // Przejście do pobierania
}

// --- POBIERANIE PDF Z BACKENDU ---
async function downloadPDF() {
    try {
        // Mapowanie danych ze store na format, którego oczekuje Twój backend (generate_pdf)
        const pdfPayload = {
            platnik_nazwa: formStore.data.notifier.businessName || '',
            platnik_adres: `${formStore.data.notifier.address.street} ${formStore.data.notifier.address.houseNumber}`,
            platnik_nip: formStore.data.notifier.nip || '',

            poszkodowany_nazwa: `${formStore.data.notifier.firstName} ${formStore.data.notifier.lastName}`,
            poszkodowany_pesel: formStore.data.victim.pesel || '',
            poszkodowany_adres: '', // Można uzupełnić jeśli jest w store
            tytul_ubezpieczenia: formStore.data.notifier.pkdCode || '',

            wypadek_zgloszenie: new Date().toLocaleDateString('pl-PL'),
            wypadek_okolicznosci: formStore.data.accident.circumstances,
            wypadek_przyczyna_bezp: formStore.data.accident.injuries, // Uproszczenie na potrzeby PDF

            swiadek_1: "Brak",
            swiadek_2: "Brak"
        }

        const response = await fetch('/raport-wypadku/api/generate-pdf/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pdfPayload)
        })

        if (!response.ok) throw new Error('Błąd generowania PDF')

        // Pobranie pliku (Blob) i wymuszenie zapisu
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `Zawiadomienie_Wypadek_${formStore.data.notifier.nip}.pdf`
        document.body.appendChild(link)
        link.click()
        window.URL.revokeObjectURL(url)

    } catch (e) {
        alert("Błąd pobierania PDF: " + e.message)
    }
}
</script>

<template>
  <div class="flex flex-col items-center gap-6 p-4 w-full">

    <!-- Progress Bar -->
    <div class="flex flex-row items-center justify-center gap-4 w-full max-w-lg mb-4">
        <div v-for="i in 4" :key="i" class="flex items-center">
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm"
                 :class="store.step >= i ? 'bg-[#006B34] text-white' : 'bg-gray-200 text-gray-500'">
                 {{ i === 4 ? '⬇' : i }}
            </div>
            <div v-if="i < 4" class="w-8 h-1" :class="store.step > i ? 'bg-[#006B34]' : 'bg-gray-200'"></div>
        </div>
    </div>

    <div class="flex flex-row w-full bg-white rounded-2xl p-6 shadow-xl min-h-[400px]">

      <!-- Robot Avatar (Lewa strona) -->
      <div class="hidden md:flex flex-col items-center pr-8 border-r border-gray-100 min-w-[200px]">
        <Robot />
        <p class="mt-4 font-bold text-[#006B34]">ZANT Asystent</p>
      </div>

      <!-- Treść (Prawa strona) -->
      <div class="flex flex-col flex-1 pl-0 md:pl-8">

        <!-- KROK -1: Powitanie -->
        <div v-if="store.step === -1">
             <h1 class="text-3xl font-extrabold text-gray-800 mb-4">Dzień dobry!</h1>
             <p class="text-lg text-gray-600 mb-6">Pomogę Ci zgłosić wypadek przy pracy. Przygotuję dokumenty i sprawdzę, czy opis zdarzenia spełnia wymogi ZUS.</p>

             <button @click="store.step = 1" class="self-start px-8 py-3 bg-[#006B34] text-white rounded-lg font-bold hover:bg-green-700 shadow-md">
                 Rozpocznij zgłoszenie
             </button>
        </div>

        <!-- KROK 1 & 2: Tekst pasywny (Formularz jest aktywny obok) -->
        <div v-if="store.step === 1 || store.step === 2">
            <h2 class="text-2xl font-bold text-gray-800 mb-2">
                {{ store.step === 1 ? 'Krok 1: Dane podstawowe' : 'Krok 2: Opis zdarzenia' }}
            </h2>
            <p class="text-gray-500">
                {{ store.step === 1 ? 'Proszę uzupełnij dane płatnika i poszkodowanego w formularzu obok.' : 'Opisz dokładnie przebieg wypadku. To najważniejsza część zgłoszenia.' }}
            </p>
            <div class="mt-8 p-4 bg-yellow-50 rounded-lg text-sm text-yellow-800 border border-yellow-200 flex gap-3">
                <span class="text-2xl">💡</span>
                <p>Wskazówka: System automatycznie pobierze dane firmy po wpisaniu NIP.</p>
            </div>
        </div>

        <!-- KROK 3: AI Konsultant (Interaktywny Czat) -->
        <div v-if="store.step === 3" class="flex flex-col h-full justify-center">

            <!-- Loader -->
            <div v-if="aiState === 'analyzing'" class="flex flex-col items-center justify-center py-10">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#006B34] mb-4"></div>
                <p class="text-lg font-medium text-gray-600">{{ aiMessage }}</p>
            </div>

            <!-- Pytanie od AI (Gdy brakuje danych) -->
            <div v-if="aiState === 'questioning'" class="animate-in fade-in slide-in-from-bottom-4 duration-500">
                <h2 class="text-xl font-bold text-orange-600 mb-4">Mam jedno pytanie...</h2>

                <div class="bg-orange-50 p-4 rounded-xl rounded-tl-none border border-orange-200 mb-6 relative">
                    <p class="text-gray-800 font-medium text-lg">"{{ aiMessage }}"</p>
                </div>

                <label class="block text-sm font-bold text-gray-600 mb-2">Twoja odpowiedź (zostanie dodana do opisu):</label>
                <div class="flex gap-2">
                    <input v-model="userResponse" @keyup.enter="submitUserResponse" type="text" placeholder="np. Tak, poślizgnąłem się na rozlanym oleju..."
                           class="flex-1 border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-orange-300 outline-none">
                    <button @click="submitUserResponse" class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600">
                        Wyślij
                    </button>
                </div>
            </div>

            <!-- Sukces -->
            <div v-if="aiState === 'success'" class="animate-in zoom-in duration-300">
                <h2 class="text-2xl font-bold text-[#006B34] mb-2">Analiza zakończona pomyślnie!</h2>
                <p class="text-gray-600 mb-6">{{ aiMessage }}</p>

                <div class="grid grid-cols-2 gap-4 mb-6">
                    <div class="p-3 bg-gray-50 rounded border flex items-center gap-2 text-green-700">✅ Nagłość</div>
                    <div class="p-3 bg-gray-50 rounded border flex items-center gap-2 text-green-700">✅ Przyczyna Zewnętrzna</div>
                    <div class="p-3 bg-gray-50 rounded border flex items-center gap-2 text-green-700">✅ Uraz</div>
                    <div class="p-3 bg-gray-50 rounded border flex items-center gap-2 text-green-700">✅ Związek z pracą</div>
                </div>

                <button @click="finishProcess" class="w-full py-3 bg-[#006B34] text-white rounded-lg font-bold hover:bg-green-700 shadow-lg">
                    Przejdź do pobierania dokumentów
                </button>
            </div>
        </div>

        <!-- KROK 4: Pobieranie -->
        <div v-if="store.step === 4">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Twoje dokumenty są gotowe</h2>
            <p class="mb-6 text-gray-600">Pobierz je, wydrukuj, podpisz i złóż w ZUS (lub wyślij przez PUE).</p>

            <div class="space-y-4">
                <div class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer group" @click="downloadPDF">
                    <div class="flex items-center gap-4">
                        <div class="bg-red-100 text-red-600 p-2 rounded">PDF</div>
                        <div>
                            <p class="font-bold text-gray-800">Zawiadomienie o wypadku (Generowane z danych)</p>
                            <p class="text-xs text-gray-500">Karta Wypadku / Zgłoszenie</p>
                        </div>
                    </div>
                    <button class="text-[#006B34] font-bold group-hover:underline">Pobierz ⬇</button>
                </div>
            </div>

            <div class="mt-8 pt-6 border-t">
                <a href="/" class="text-gray-500 hover:text-black text-sm">← Wróć do strony głównej</a>
            </div>
        </div>

      </div>
    </div>
  </div>
</template>