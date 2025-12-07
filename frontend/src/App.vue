<template>
  <!-- SCENARIO A: ZUS WORKER VIEW (Analyzer) -->
  <div v-if="isWorkerView" class="w-full min-h-screen bg-gray-100 p-6">
    <AnalyzerForm />
  </div>

  <!-- SCENARIO B: CLIENT VIEW (Wizard) -->
  <div v-else class="flex flex-col min-h-screen">
    <main class="flex flex-col w-full flex-1 p-6 gap-6 lg:flex-row lg:justify-center">
      <!-- left: start form / steps -->
      <div class="flex-1">
        <StartForm :step="store.step" />
      </div>

      <!-- right: form panel -->
      <div class="flex-1">
        <!-- Form 1: Notification -->
        <AccidentNotificationForm
          v-if="shouldShowAccidentForm"
          :step="store.step"
        />

        <!-- Form 2: Explanation -->
        <VictimExplanationForm
          v-if="shouldShowVictimForm"
        />
      </div>
    </main>

    <footer>
      <Footer />
    </footer>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { store } from '@/stores/step.js'
import Footer from "@/components/Footer.vue";
import StartForm from "@/components/StartForm.vue";
import AccidentNotificationForm from "@/components/AccidentNotificationForm.vue";
import VictimExplanationForm from "@/components/VictimExplanationForm.vue";
// Import the existing Analyzer component
import AnalyzerForm from "@/components/AnalyzerForm.vue";

// Detect if we are on the /ocena-wypadku/ URL
const isWorkerView = ref(false)

onMounted(() => {
  // Simple check: does the URL contain 'ocena-wypadku'?
  if (window.location.pathname.includes('ocena-wypadku')) {
    isWorkerView.value = true
  }
})

// Logic for Client View
const shouldShowAccidentForm = computed(() => {
  if (store.step === 2) return false;
  return true;
})

const shouldShowVictimForm = computed(() => {
  return store.step === 2;
})
</script>

<style scoped>
/* Scoped styles mainly handled by Tailwind classes in template */
</style>