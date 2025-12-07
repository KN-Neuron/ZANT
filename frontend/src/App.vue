<script setup>
import { ref } from 'vue'
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import Robot from "@/components/Robot.vue";
import StartForm from "@/components/StartForm.vue";
import AccidentNotificationForm from "@/components/AccidentNotificationForm.vue";
import VictimExplanationForm from "@/components/VictimExplanationForm.vue";

const currentView = ref('start'); // 'start' | 'forms'
const activeForms = ref([]); // ['accident', 'victim']
const activeTab = ref('');

const handleStartProcess = (selected) => {
  activeForms.value = selected;
  if (selected.length > 0) {
    currentView.value = 'forms';
    activeTab.value = selected[0];
  }
};

const switchTab = (tab) => {
  activeTab.value = tab;
};

const goBack = () => {
  currentView.value = 'start';
  activeForms.value = [];
};
</script>

<style scoped lang="postcss">
  header {
    line-height: 1.5;
  }

  .logo {
    display: block;
    margin: 0 auto 2rem;
  }

  @media (min-width: 1024px) {
    header {
      display: flex;
      place-items: center;
      padding-right: calc(var(--section-gap) / 2);
    }

    .logo {
      margin: 0 2rem 0 0;
    }

    header .wrapper {
      display: flex;
      place-items: flex-start;
      flex-wrap: wrap;
    }
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
</style>

<template>
  <main class="min-h-screen flex flex-col relative overflow-hidden bg-gray-50">
    <div class="container mx-auto px-4 py-8 z-10 flex-grow">

      <!-- Top Navigation / Status -->
      <Header />

      <!-- Robot Character (Always visible but positioned) -->
      <div class="absolute top-24 left-4 hidden lg:block z-0 pointer-events-none opacity-80">
         <Robot />
      </div>

      <!-- Main Content Area -->
      <div class="mt-12 w-full flex justify-center">

        <!-- View: Start Selection -->
        <Transition name="fade" mode="out-in">
          <StartForm
            v-if="currentView === 'start'"
            @start-process="handleStartProcess"
          />

          <!-- View: Forms -->
          <div v-else class="w-full max-w-6xl">

            <!-- Navigation Tabs -->
            <div class="flex items-center justify-between mb-6">
               <button @click="goBack" class="text-gray-500 hover:text-black flex items-center gap-2 font-medium transition-colors">
                  ← Back to selection
               </button>

               <div v-if="activeForms.length > 1" class="flex gap-2 bg-white p-1 rounded-lg shadow-sm border">
                  <button
                    v-for="form in activeForms"
                    :key="form"
                    @click="switchTab(form)"
                    :class="[
                      'px-4 py-2 rounded-md text-sm font-bold transition-all',
                      activeTab === form ? 'bg-green-600 text-white shadow' : 'text-gray-600 hover:bg-gray-100'
                    ]"
                  >
                    {{ form === 'accident' ? 'Zawiadomienie (ZUS)' : 'Wyjaśnienia Poszkodowanego' }}
                  </button>
               </div>
            </div>

            <!-- Form Rendering -->
            <div class="transition-all duration-300">
              <AccidentNotificationForm v-if="activeTab === 'accident'" />
              <VictimExplanationForm v-if="activeTab === 'victim'" />
            </div>

          </div>
        </Transition>
      </div>

    </div>

    <Footer />
  </main>
</template>