<script setup>
import { ref, watch } from 'vue' // Dodajemy watch
import { store } from '@/stores/step.js'
import { useFormStore } from '@/stores/form.js'
import Robot from './Robot.vue'

// UWAGA: Usuwamy lokalne 'selectedForms = ref([])' i używamy store.selectedForms
const formStore = useFormStore()

// State walidacji
const isValidating = ref(false)
const validationFeedback = ref(null)
const isComplete = ref(false)

// Watcher: Jeśli ktoś (np. formularz obok) ustawi triggerValidation na true, uruchom sprawdzanie
watch(() => store.triggerValidation, (newVal) => {
  if (newVal === true) {
    // Przełącz na krok weryfikacji jeśli jeszcze tam nie jesteśmy
    store.step = 3
    validateData()
    // Reset flagi
    store.triggerValidation = false
  }
})

function previousStep() {
  // Logika powrotu: z 3 -> 2 (jeśli wybrano Wyjaśnienia) lub z 3 -> 1
  if (store.step === 3) {
    if (store.selectedForms.includes('Victim report')) {
      store.step = 2
    } else {
      store.step = 1
    }
  } else if (store.step === 2) {
    store.step = 1
  } else {
    store.step--
  }

  // Reset walidacji przy powrocie
  if (store.step < 3) {
    resetValidation()
  }
}

function nextStep() {
  // Logika Dalej:
  // -1 -> 0
  // 0 -> 1
  // 1 -> 2 (jeśli wybrano Wyjaśnienia) LUB -> 3
  // 2 -> 3

  if (store.step === -1) {
    store.step = 0
  } else if (store.step === 0) {
    store.step = 1
  } else if (store.step === 1) {
    if (store.selectedForms.includes('Victim report')) {
      store.step = 2
    } else {
      store.step = 3
    }
  } else if (store.step === 2) {
    store.step = 3
  }
}

function resetValidation() {
  validationFeedback.value = null
  isComplete.value = false
  isValidating.value = false
}

async function validateData() {
  isValidating.value = true
  validationFeedback.value = null

  try {
    const payload = {
      notification_desc: formStore.data.accident.circumstances || "",
      injuries: formStore.data.accident.injuries || "",
      activities: "",
      external_cause: ""
    }

    const response = await fetch('/raport-wypadku/api/validate/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!response.ok) throw new Error('Błąd serwera')
    const result = await response.json()

    validationFeedback.value = result.feedback
    isComplete.value = result.is_complete

  } catch (error) {
    console.error(error)
    validationFeedback.value = "Błąd asystenta AI. Spróbuj ponownie."
    isComplete.value = false
  } finally {
    isValidating.value = false
  }
}

function forceSubmit() {
  alert('Generowanie dokumentów PDF...')
  // Tutaj logika pobierania
  resetValidation()
}
</script>

<template>
  <div class="flex flex-col items-center gap-6 p-4 w-full">

    <!-- top step bar -->
    <div class="flex flex-col items-center gap-2 w-full">
      <div class="flex flex-row items-center justify-center gap-4 w-full">
        <template v-for="i in 3" :key="i">
          <div class="flex flex-col items-center">
            <div
              class="flex w-14 h-14 rounded-full justify-center items-center"
              :class="store.step >= i ? 'bg-green-500' : 'bg-gray-300'"
            >
              <span class="text-white font-bold text-xl">{{ i }}</span>
            </div>
          </div>
          <div v-if="i < 3" class="flex-1 h-1 bg-gray-300 rounded"></div>
        </template>
      </div>
    </div>

    <!-- panel content -->
    <div class="flex flex-row w-full bg-white rounded-2xl p-6 shadow">
      <!-- Robot zawsze widoczny -->
      <Robot class="pl-4 pr-12" />

      <div class="flex flex-col justify-between w-full">

        <div class="flex flex-col">

          <!-- Krok -1: Wybór -->
          <div v-if="store.step === -1">
            <h1 class="text-2xl sm:text-3xl font-extrabold text-black pb-4">Cześć, jestem ZANT!</h1>
            <p class="text-gray-600 mt-2">Jestem asystentem ds. wypadków. Co chcesz wypełnić?</p>
            <div class="flex flex-col gap-3 mt-4 p-4">
              <label class="flex items-center gap-3 cursor-pointer">
                <!-- ZAWSZE ZAZNACZONE (główny formularz) -->
                <input type="checkbox" checked disabled class="h-5 w-5 text-blue-600 rounded opacity-50">
                <span class="text-black font-medium">Zawiadomienie o wypadku (Obowiązkowe)</span>
              </label>

              <label class="flex items-center gap-3 cursor-pointer">
                <!-- OPCJONALNE -->
                <input
                  type="checkbox"
                  class="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
                  v-model="store.selectedForms"
                  value="Victim report"
                />
                <span class="text-black font-medium">Wyjaśnienia poszkodowanego (Opcjonalne)</span>
              </label>
            </div>
          </div>

          <!-- Krok 0: Potwierdzenie -->
          <div v-if="store.step === 0">
            <h1 class="text-2xl font-extrabold pb-4">Zaczynajmy!</h1>
            <p class="text-gray-600">Wypełnimy Zawiadomienie o wypadku.</p>
            <p v-if="store.selectedForms.includes('Victim report')" class="text-gray-600">
              Oraz Wyjaśnienia poszkodowanego.
            </p>
          </div>

          <!-- Krok 1: Zawiadomienie -->
          <div v-if="store.step === 1">
            <h1 class="text-2xl font-extrabold pb-4">Krok 1: Zawiadomienie</h1>
            <p class="text-gray-600">Wypełnij dane w formularzu po prawej stronie.</p>
          </div>

          <!-- Krok 2: Wyjaśnienia (tylko jeśli wybrano) -->
          <div v-if="store.step === 2">
            <h1 class="text-2xl font-extrabold pb-4">Krok 2: Wyjaśnienia</h1>
            <p class="text-gray-600">Teraz uzupełnij wyjaśnienia poszkodowanego.</p>
          </div>

          <!-- Krok 3: Walidacja -->
          <div v-if="store.step === 3">
            <h2 class="text-2xl font-bold mb-4">Weryfikacja</h2>

            <div v-if="isValidating" class="text-blue-600 animate-pulse">
              Analizuję zgodność opisu z definicją wypadku...
            </div>

            <div v-else-if="validationFeedback">
              <p class="font-bold text-lg mb-2" :class="isComplete ? 'text-green-600' : 'text-orange-600'">
                {{ isComplete ? 'Analiza pomyślna!' : 'Mam uwagi:' }}
              </p>
              <div class="text-gray-700 italic bg-gray-50 p-3 rounded border text-sm">
                {{ validationFeedback }}
              </div>
            </div>

            <p v-else class="mt-2 text-gray-600">
              Kliknij "Sprawdź", aby zweryfikować opis zdarzenia.
            </p>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex justify-between w-full pt-6">
          <button v-if="store.step !== -1" class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                  @click="previousStep" :disabled="isValidating">
            Wstecz
          </button>

          <button v-if="store.step < 3" class="ml-auto bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                  @click="nextStep">
            Dalej
          </button>

          <div v-if="store.step === 3" class="ml-auto flex gap-2">
            <button v-if="!validationFeedback" class="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
                    @click="validateData" :disabled="isValidating">
              Sprawdź
            </button>
            <button v-else class="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600" @click="forceSubmit">
              Pobierz PDF
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>