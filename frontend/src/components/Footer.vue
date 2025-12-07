<template>
  <footer class="w-full bg-[#006B34] text-white py-8 px-6">
    <div
      class="max-w-screen-xl mx-auto flex flex-col lg:flex-row items-start justify-between gap-8"
    >
      <!-- left column -->
      <ul class="flex flex-col gap-3 text-sm">
        <li class="flex items-center gap-2 cursor-pointer hover:underline">
          <span>›</span> Zamówienia publiczne
        </li>
        <li class="flex items-center gap-2 cursor-pointer hover:underline">
          <span>›</span> Praca w ZUS
        </li>
        <li class="flex items-center gap-2 cursor-pointer hover:underline">
          <span>›</span> Praca dla lekarzy
        </li>
        <li class="flex items-center gap-2 cursor-pointer hover:underline">
          <span>›</span> Konkursy ofert
        </li>
        <li class="flex items-center gap-2 cursor-pointer hover:underline">
          <span>›</span> Mienie zbędne
        </li>
        <li class="flex items-center gap-2 cursor-pointer hover:underline">
          <span>›</span> Mapa serwisu
        </li>
      </ul>

      <!-- middle icons -->
      <div
        class="flex flex-wrap items-center gap-6 text-sm border-l border-white/30 pl-6"
      >
        <span class="cursor-pointer hover:underline">Deklaracja dostępności</span>
        <span class="cursor-pointer hover:underline">Ustawienia plików cookies</span>
    </div>

        <!-- icons row -->
        <div class="flex items-center gap-6">
          <span class="flex items-center gap-2 cursor-pointer">
            <div class="w-7 h-7 rounded-full bg-white flex items-center justify-center">
              ▶
            </div>
            Elektroniczny ZUS
          </span>

          <span class="flex items-center gap-2 cursor-pointer">
            <div class="w-7 h-7 rounded-full bg-white flex items-center justify-center text-[#006B34] font-bold">
              in
            </div>
            Linkedin
          </span>

          <span class="flex items-center gap-2 cursor-pointer">
            <div class="w-7 h-7 rounded-full bg-white flex items-center justify-center text-[#006B34] font-bold">
              X
            </div>
            X
          </span>

          <span class="flex items-center gap-2 cursor-pointer">
            <div class="w-7 h-7 rounded-full bg-white flex items-center justify-center text-[#006B34]">
              rss
            </div>
            Kanał RSS
          </span>
        </div>
      </div>

      <!-- right "to top" -->
      <div class="flex flex-col items-center gap-2 ml-auto">
        <button
          @click="scrollTop"
          class="w-10 h-10 rounded-full border border-white flex items-center justify-center hover:bg-white/10"
        >
          ↑
        </button>
        <span class="text-sm cursor-pointer hover:underline">Do góry</span>
      </div>
  </footer>
</template>

<script setup>
function scrollTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}
</script>
