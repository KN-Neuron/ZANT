<template>
  <main class="flex flex-col w-full min-h-screen p-6 gap-6">

    <!-- left: start form / steps -->
    <div class="flex-1">
      <StartForm :step="step" @update:step="val => step = val" />
    </div>

    <!-- right: form panel -->
    <div class="flex-1">
      <AccidentNotificationForm :step="step" />
    </div>

  </main>

  <footer>
    <Footer />
  </footer>
</template>

<script setup>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import Robot from "@/components/Robot.vue";
import StartForm from "@/components/StartForm.vue";
import AccidentNotificationForm from "@/components/AccidentNotificationForm.vue";
</script>

<style scoped>
main {
  display: flex;
  flex-direction: column;
}

@media (min-width: 1024px) {
  main {
    flex-direction: row;
    justify-content: center;
  }
}
</style>
