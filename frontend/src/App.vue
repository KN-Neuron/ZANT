<script setup>
  import Header from "@/components/Header.vue";
  import Footer from "@/components/Footer.vue";
  // import AnalyzerForm from "@/components/AnalyzerForm.vue";
  import Robot from "@/components/Robot.vue";
  import StartForm from "@/components/StartForm.vue";
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
</style>

<template>

  <main>
    <!-- <AnalyzerForm /> -->
    <Header />
    <Robot />
    <StartForm />
  </main>

  <footer>
    <Footer />
  </footer>
</template>
