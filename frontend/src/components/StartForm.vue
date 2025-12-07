<template>
  <div class="flex flex-col items-center gap-6 p-4 w-full">

    <!-- responsive content card -->
    <div class="w-full max-w-md bg-white rounded-2xl p-6 shadow">
      <h1 class="text-2xl sm:text-3xl font-extrabold text-black pb-4">
        Hello, my name is ZANT!
      </h1>
      <p class="text-gray-600 mt-2 text-sm sm:text-base leading-relaxed">
        An assistant to aid you with filling out your workplace accident form.
      </p>
      <p class="text-gray-600 mt-2 text-sm sm:text-base leading-relaxed">
        Which form(s) would you like to fill out?
      </p>

      <div class="flex flex-col gap-3 mt-4 p-4">

        <label class="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            class="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
            v-model="selectedForms"
            value="accident"
          />
          <span class="text-black font-medium">
            Workplace accident notification
          </span>
        </label>

        <label class="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            class="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
            v-model="selectedForms"
            value="victim"
          />
          <span class="text-black font-medium">
            Victim report
          </span>
        </label>

      </div>

      <button class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded mt-6">
        Next
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue"

const selectedForms = ref([])
</script>
