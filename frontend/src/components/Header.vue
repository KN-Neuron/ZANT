<template>
    <!-- responsive step timeline -->
    <div class="flex flex-wrap items-center justify-center gap-4">
      <template v-for="i in 5" :key="i">
        <div class="flex flex-col items-center">
          <div class="flex w-14 h-14 sm:w-16 sm:h-16 bg-gray-300 rounded-full justify-center items-center">
            <span class="text-black text-xl font-semibold">{{ i }}</span>
          </div>
        </div>
        <div v-if="i !== 5" class="w-10 sm:w-12 h-1 bg-gray-300"></div>
      </template>
    </div>
</template>