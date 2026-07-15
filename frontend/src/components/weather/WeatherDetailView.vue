<script setup>
import { onMounted } from 'vue'
import { useWeather } from '../../composables/useWeather'

defineEmits(['back'])

const { weatherData, hourlyForecast, dailyForecast, isDetailLoading, fetchForecastDetail } = useWeather()

onMounted(() => {
  fetchForecastDetail()
})

const dayLabel = (dateStr) => {
  const date = new Date(dateStr)
  if (date.toDateString() === new Date().toDateString()) return '오늘'
  return date.toLocaleDateString('ko-KR', { weekday: 'short' })
}

const dateLabel = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}.${date.getDate()}`
}
</script>

<template>
  <section class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10 animate-fade-in">
    <button
      @click="$emit('back')"
      class="flex items-center gap-2 text-sm font-semibold text-slate-600 hover:text-blue-600 transition"
    >
      <i class="fa-solid fa-arrow-left"></i> 뒤로가기
    </button>

    <div
      class="bg-gradient-to-tr from-blue-600 to-sky-500 rounded-3xl p-8 text-white shadow-lg shadow-blue-500/20 flex items-center justify-between"
    >
      <div>
        <p class="text-sm font-semibold text-blue-100">서울특별시</p>
        <p class="text-5xl font-black mt-2">{{ weatherData.temp }}°C</p>
        <p class="text-sm font-medium text-blue-50 mt-1">{{ weatherData.status }}</p>
      </div>
      <div class="text-6xl">{{ weatherData.icon }}</div>
    </div>

    <div class="space-y-4">
      <h3 class="text-lg font-black text-slate-900">시간별 예보</h3>
      <p v-if="isDetailLoading" class="text-sm text-slate-400">불러오는 중...</p>
      <div v-else class="flex gap-3 overflow-x-auto pb-2">
        <div
          v-for="hour in hourlyForecast"
          :key="hour.time"
          class="flex-shrink-0 w-20 bg-white border border-slate-100 rounded-2xl py-4 px-2 text-center shadow-sm"
        >
          <p class="text-xs font-semibold text-slate-500">{{ hour.hourLabel }}</p>
          <p class="text-2xl my-2">{{ hour.icon }}</p>
          <p class="text-sm font-bold text-slate-900">{{ hour.temp }}°</p>
          <p class="text-[11px] text-sky-600 font-semibold mt-1">{{ hour.pop }}%</p>
        </div>
      </div>
    </div>

    <div class="space-y-4">
      <h3 class="text-lg font-black text-slate-900">주간 예보 (7일)</h3>
      <p v-if="isDetailLoading" class="text-sm text-slate-400">불러오는 중...</p>
      <div v-else class="bg-white border border-slate-100 rounded-2xl divide-y divide-slate-100">
        <div v-for="day in dailyForecast" :key="day.date" class="flex items-center justify-between px-6 py-4">
          <div class="w-16 text-sm font-bold text-slate-800">
            {{ dayLabel(day.date) }}
            <span class="block text-xs font-normal text-slate-400">{{ dateLabel(day.date) }}</span>
          </div>
          <div class="text-2xl">{{ day.icon }}</div>
          <div class="text-xs font-semibold text-sky-600 w-12 text-right">{{ day.pop }}%</div>
          <div class="text-sm font-bold text-slate-900 w-24 text-right">
            {{ day.tempMax }}° <span class="text-slate-400 font-medium">/ {{ day.tempMin }}°</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
