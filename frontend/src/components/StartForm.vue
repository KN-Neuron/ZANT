<template>
  <div class="flex flex-col items-center gap-6 p-4 w-full">

    <!-- top step bar with robot -->
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

          <!-- separator, but not after last item -->
          <div
            v-if="i < 3"
            class="flex-1 h-1 bg-gray-300 rounded"
          ></div>
          </template>
        </div>
      </div>

    <!-- panel content -->
    <div class="flex flex-row w-full bg-white rounded-2xl p-6 shadow">
    <Robot class="pl-4 pr-12" />

    <div class="flex flex-col justify-between w-full">

        <!-- step content -->
        <div class="flex flex-col">
        <div v-if="store.step === -1">
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
                value="Workplace accident notification"
                />
                <span class="text-black font-medium">Workplace accident notification</span>
            </label>

            <label class="flex items-center gap-3 cursor-pointer">
                <input
                type="checkbox"
                class="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
                v-model="selectedForms"
                value="Victim report"
                />
                <span class="text-black font-medium">Victim report</span>
            </label>
            </div>
        </div>

        <div v-if="store.step === 0">
            <h1 class="text-2xl sm:text-3xl font-extrabold text-black pb-4">
            Fantastic! Let's get started.
            </h1>
            <p class="mt-2 text-gray-600">Just to make sure: you're filling out:</p>
            <ul>
                <li class="mt-2 text-gray-600" v-for="form in selectedForms" :key="form"><pre>    •  {{ form }}</pre></li>
            </ul>
            <p class="mt-2 text-gray-600">If that's not the correct form, please go back and change your selection!</p>
        </div>

        <div v-if="store.step === 1">
            <h1 class="text-2xl sm:text-3xl font-extrabold text-black pb-4">
            Please provide the victim's details.
            </h1>
            <p class="mt-2 text-gray-600">NOTE: If the affected person does not have the PESEL number, please provide a number of a valid ID document.</p>
        </div>

        <div v-if="store.step === 2">
            <h1 class="text-2xl sm:text-3xl font-extrabold text-black pb-4">
            Fantastic! Let's get started.
            </h1>
            <p class="mt-2 text-gray-600">Here you can add the form details...</p>
        </div>

        <div v-if="store.step === 3">
            <h2 class="text-2xl font-bold">Step 3: review & submit</h2>
            <p class="mt-2 text-gray-600">Review your choices and submit the form.</p>
        </div>
        </div>

        <!-- bottom buttons -->
        <div class="flex justify-between w-full pt-6">
        <button
            v-if="store.step !== -1"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
            @click="previousStep"
        >
            Back
        </button>

        <button
            v-if="store.step !== 3"
            :disabled="selectedForms.length === 0"
            class="ml-auto bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
            @click="nextStep"
        >
            Next
        </button>

        <button
            v-if="store.step === 3"
            class="ml-auto bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded"
            @click="finish"
        >
            Submit
        </button>
        </div>

    </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { store } from '@/stores/step.js'
import Robot from './Robot.vue' // your waving robot component

const selectedForms = ref([])

function previousStep() {
  store.step--
}

function nextStep() {
  store.step++
}

function finish() {
  alert('Form submitted: ' + selectedForms.value.join(', '))
  store.step = -1
  selectedForms.value = []
}
</script>
