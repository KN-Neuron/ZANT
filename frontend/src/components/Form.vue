<template>
  <div class="bg-white rounded-2xl shadow p-6 w-full">
    <h2 class="text-2xl font-bold mb-4">Accident Report Form</h2>

    <form @submit.prevent="submitForm" class="flex flex-col gap-4">
      <div>
        <label class="block text-gray-700 font-medium mb-1">Full Name</label>
        <input
          type="text"
          v-model="formData.name"
          placeholder="Your full name"
          class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-gray-700 font-medium mb-1">Date of Accident</label>
        <input
          type="date"
          v-model="formData.date"
          class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-gray-700 font-medium mb-1">Description</label>
        <textarea
          v-model="formData.description"
          placeholder="Brief description of the accident"
          class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows="4"
        ></textarea>
      </div>

      <div>
        <label class="block text-gray-700 font-medium mb-1">Injuries?</label>
        <select
          v-model="formData.injuries"
          class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select</option>
          <option value="none">None</option>
          <option value="minor">Minor</option>
          <option value="major">Major</option>
        </select>
      </div>

      <button
        type="submit"
        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded mt-2 self-start"
      >
        Submit
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const formData = reactive({
  name: '',
  date: '',
  description: '',
  injuries: '',
})

function submitForm() {
  alert(`Form submitted!\n${JSON.stringify(formData, null, 2)}`)
  formData.name = ''
  formData.date = ''
  formData.description = ''
  formData.injuries = ''
}
</script>
