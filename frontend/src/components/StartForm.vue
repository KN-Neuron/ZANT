<template>
  <div class="flex flex-col items-center gap-6 p-4 w-full">

    <div class="w-full max-w-md bg-white rounded-2xl p-6 shadow-xl border border-gray-100 relative z-10">
      <h1 class="text-2xl sm:text-3xl font-extrabold text-gray-800 pb-4 text-center">
        Hello, my name is ZANT!
      </h1>
      <p class="text-gray-600 mt-2 text-sm sm:text-base leading-relaxed text-center">
        An assistant to aid you with filling out your workplace accident form.
      </p>
      <div class="w-16 h-1 bg-green-500 mx-auto my-4 rounded-full"></div>

      <p class="text-gray-700 font-semibold mt-2 text-sm sm:text-base leading-relaxed">
        Which form(s) would you like to fill out?
      </p>

      <div class="flex flex-col gap-3 mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">

        <label class="flex items-center gap-3 cursor-pointer p-2 hover:bg-gray-100 rounded transition-colors">
          <input
            type="checkbox"
            class="h-5 w-5 text-green-600 rounded focus:ring-green-500 cursor-pointer border-gray-300"
            v-model="selectedForms"
            value="accident"
          />
          <span class="text-gray-800 font-medium">
            Zawiadomienie o wypadku (ZUS EWYP)
          </span>
        </label>

        <label class="flex items-center gap-3 cursor-pointer p-2 hover:bg-gray-100 rounded transition-colors">
          <input
            type="checkbox"
            class="h-5 w-5 text-green-600 rounded focus:ring-green-500 cursor-pointer border-gray-300"
            v-model="selectedForms"
            value="victim"
          />
          <span class="text-gray-800 font-medium">
            Zapis wyjaśnień poszkodowanego
          </span>
        </label>

      </div>

      <button
        @click="proceed"
        :disabled="selectedForms.length === 0"
        class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg mt-6 shadow-md transition-all transform hover:scale-[1.02] active:scale-95">
        Rozpocznij wypełnianie
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue"

const emit = defineEmits(['start-process'])
const selectedForms = ref([])

const proceed = () => {
  if (selectedForms.value.length > 0) {
    emit('start-process', selectedForms.value)
  }
}
</script>