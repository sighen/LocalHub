<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { heroSlides } from '../../data/mockData'

const emit = defineEmits(['scroll-to-upcoming', 'go-community'])

const heroIndex = ref(0)
let autoSlideTimer = null

const prevHero = () => {
  heroIndex.value = (heroIndex.value - 1 + heroSlides.length) % heroSlides.length
}
const nextHero = () => {
  heroIndex.value = (heroIndex.value + 1) % heroSlides.length
}

onMounted(() => {
  autoSlideTimer = setInterval(() => {
    heroIndex.value = (heroIndex.value + 1) % heroSlides.length
  }, 4500)
})

onUnmounted(() => {
  clearInterval(autoSlideTimer)
})
</script>

<template>
  <div class="relative overflow-hidden bg-slate-950 h-[480px] text-white flex items-center">
    <div class="absolute inset-0 opacity-50">
      <transition name="hero-fade">
        <div
          :key="heroIndex"
          class="absolute inset-0 bg-cover bg-center"
          :style="{ backgroundImage: `url(${heroSlides[heroIndex].img})` }"
        ></div>
      </transition>
    </div>
    <div class="absolute inset-0 bg-gradient-to-r from-slate-950/90 via-slate-900/60 to-transparent"></div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full z-10 space-y-6">
      <transition name="hero-text-fade" mode="out-in">
        <div :key="heroIndex" class="space-y-6">
          <span class="inline-flex items-center gap-1.5 px-3 py-1 bg-white/10 text-white rounded-full text-xs font-bold border border-white/20 uppercase tracking-wider backdrop-blur-sm">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> {{ heroSlides[heroIndex].tag }}
          </span>
          <h1 class="text-4xl sm:text-5xl font-black tracking-tight leading-none text-white drop-shadow-md">
            {{ heroSlides[heroIndex].titleLine1 }}<br />
            <span class="text-blue-400">{{ heroSlides[heroIndex].titleLine2 }}</span>
          </h1>
          <p class="text-base sm:text-lg text-slate-200 max-w-lg leading-relaxed font-medium">
            {{ heroSlides[heroIndex].desc }}
          </p>
        </div>
      </transition>
      <div class="flex gap-3">
        <button
          @click="emit('scroll-to-upcoming')"
          class="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold shadow-lg shadow-blue-600/30 transition duration-150 transform hover:-translate-y-0.5"
        >
          진행중인 이벤트 보기
        </button>
        <button
          @click="emit('go-community')"
          class="px-6 py-3 bg-white/10 hover:bg-white/20 text-white border border-white/30 rounded-xl font-bold transition duration-150 backdrop-blur-sm"
        >
          익명 소통 참여
        </button>
      </div>
    </div>

    <div class="absolute bottom-6 left-1/2 transform -translate-x-1/2 flex items-center gap-6 z-10 bg-black/30 px-6 py-2 rounded-full backdrop-blur-md border border-white/10">
      <button @click="prevHero" class="text-white/70 hover:text-white transition text-xs"><i class="fa-solid fa-chevron-left"></i></button>
      <div class="flex gap-2">
        <span
          v-for="(slide, idx) in heroSlides"
          :key="idx"
          @click="heroIndex = idx"
          :class="['w-2 h-2 rounded-full cursor-pointer transition-all duration-300', heroIndex === idx ? 'bg-blue-500 w-6' : 'bg-white/50']"
        ></span>
      </div>
      <button @click="nextHero" class="text-white/70 hover:text-white transition text-xs"><i class="fa-solid fa-chevron-right"></i></button>
    </div>
  </div>
</template>

<style scoped>
.hero-fade-enter-active,
.hero-fade-leave-active {
  transition: opacity 1.1s ease;
}
.hero-fade-enter-from,
.hero-fade-leave-to {
  opacity: 0;
}

.hero-text-fade-enter-active,
.hero-text-fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.hero-text-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.hero-text-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
