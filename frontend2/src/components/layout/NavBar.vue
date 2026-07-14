<script setup>
import { ref } from 'vue'
import { useWeather } from '../../composables/useWeather'

const props = defineProps({
  currentTab: { type: String, required: true }
})
const emit = defineEmits(['update:currentTab', 'open-calendar', 'open-map'])

const { weatherData, toggleWeatherDetail } = useWeather()

const isMobileMenuOpen = ref(false)

const setTab = (tab) => {
  emit('update:currentTab', tab)
  isMobileMenuOpen.value = false
}

const openCalendar = () => {
  emit('open-calendar')
  isMobileMenuOpen.value = false
}

const openMap = () => {
  emit('open-map')
  isMobileMenuOpen.value = false
}
</script>

<template>
  <nav class="bg-white/95 backdrop-blur-md border-b border-slate-100 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center gap-3">
          <div class="bg-gradient-to-tr from-blue-600 to-sky-500 p-2.5 rounded-xl text-white shadow-md shadow-blue-500/20">
            <i class="fa-solid fa-map-location-dot text-lg"></i>
          </div>
          <div>
            <span class="text-xl font-black tracking-tight text-slate-900">Local<span class="text-blue-600">Hub</span></span>
            <span class="ml-1 text-[10px] px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full font-bold">SEOUL</span>
          </div>
        </div>

        <div class="hidden md:flex space-x-1 bg-slate-100 p-1 rounded-xl">
          <button
            @click="setTab('home')"
            :class="['px-5 py-2 text-sm font-semibold rounded-lg transition-all duration-200', currentTab === 'home' ? 'text-blue-600 bg-white shadow-sm' : 'text-slate-600 hover:text-slate-900 hover:bg-white/50']"
          >
            지금의 서울 (홈)
          </button>
          <button @click="openCalendar" class="px-5 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:text-slate-900 hover:bg-white/50 transition duration-200">
            축제 캘린더
          </button>
          <button @click="openMap" class="px-5 py-2 text-sm font-semibold rounded-lg text-slate-600 hover:text-slate-900 hover:bg-white/50 transition duration-200">
            맛집·관광 명소 지도
          </button>
          <button
            @click="setTab('community')"
            :class="['px-5 py-2 text-sm font-semibold rounded-lg transition-all duration-200', currentTab === 'community' ? 'text-blue-600 bg-white shadow-sm' : 'text-slate-600 hover:text-slate-900 hover:bg-white/50']"
          >
            익명 소통방 (CRUD)
          </button>
        </div>

        <div class="flex items-center gap-4">
          <div
            @click="toggleWeatherDetail"
            class="cursor-pointer flex items-center gap-2 px-3 py-1.5 bg-sky-50 hover:bg-sky-100 rounded-xl text-sky-700 text-xs font-bold border border-sky-100 transition"
          >
            <span>{{ weatherData.icon }}</span>
            <span>서울 {{ weatherData.temp }}°C</span>
          </div>
          <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="md:hidden p-2 text-slate-600 hover:text-slate-900 rounded-lg bg-slate-50 border border-slate-100">
            <i class="fa-solid fa-bars text-lg"></i>
          </button>
        </div>
      </div>
    </div>

    <div v-if="isMobileMenuOpen" class="md:hidden border-t border-slate-100 bg-white px-4 py-3 space-y-2">
      <button @click="setTab('home')" class="w-full text-left px-4 py-2.5 text-sm font-semibold rounded-lg text-slate-700 hover:bg-slate-50 flex items-center">
        <i class="fa-solid fa-house w-6 text-blue-600"></i> 지금의 서울 (홈)
      </button>
      <button @click="openCalendar" class="w-full text-left px-4 py-2.5 text-sm font-semibold rounded-lg text-slate-700 hover:bg-slate-50 flex items-center">
        <i class="fa-solid fa-calendar w-6 text-emerald-600"></i> 축제 캘린더
      </button>
      <button @click="openMap" class="w-full text-left px-4 py-2.5 text-sm font-semibold rounded-lg text-slate-700 hover:bg-slate-50 flex items-center">
        <i class="fa-solid fa-map-location-dot w-6 text-indigo-600"></i> 맛집·관광 명소 지도
      </button>
      <button @click="setTab('community')" class="w-full text-left px-4 py-2.5 text-sm font-semibold rounded-lg text-slate-700 hover:bg-slate-50 flex items-center">
        <i class="fa-solid fa-comments w-6 text-purple-600"></i> 익명 소통방 (CRUD)
      </button>
    </div>
  </nav>
</template>
