<script setup>
import { useEvents } from '../../composables/useEvents'

const emit = defineEmits(['open-calendar'])

const { year, month, daysInMonth, selectedDate, filteredEvents, getWeekdayLabel, dateStrFor, goToMonth, openEventDetails } =
  useEvents()
</script>

<template>
  <section id="upcoming-section" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
    <div class="text-center space-y-2">
      <span class="text-xs font-extrabold text-blue-600 uppercase tracking-widest">서울에서 진행되는 다양한 이벤트</span>
      <h2 class="text-3xl font-black text-slate-900 tracking-tight">서울 Upcoming!</h2>
    </div>

    <div class="bg-white border border-slate-100 rounded-2xl p-4 shadow-sm flex items-center gap-3">
      <div class="bg-slate-100 px-4 py-2 rounded-xl text-center shrink-0">
        <span class="text-[10px] text-slate-400 font-bold block uppercase">{{ year }}</span>
        <div class="flex items-center justify-center gap-3">
          <button @click="goToMonth(-1)" class="text-slate-400 hover:text-slate-700 font-black text-sm transition px-0.5">&lt;</button>
          <span class="text-lg font-black text-slate-800">{{ String(month).padStart(2, '0') }}월</span>
          <button @click="goToMonth(1)" class="text-slate-400 hover:text-slate-700 font-black text-sm transition px-0.5">&gt;</button>
        </div>
      </div>

      <div class="flex-grow overflow-x-auto flex gap-2 py-1 custom-scrollbar scroll-smooth">
        <button
          v-for="day in daysInMonth"
          :key="day"
          @click="selectedDate = dateStrFor(day)"
          :class="['px-4 py-2.5 rounded-xl text-center min-w-[56px] transition duration-150 shrink-0 border', selectedDate === dateStrFor(day) ? 'bg-blue-600 border-blue-600 text-white font-bold shadow-md shadow-blue-500/10' : 'bg-slate-50 border-slate-100 text-slate-600 hover:bg-slate-100']"
        >
          <span class="text-xs block opacity-80">{{ getWeekdayLabel(day) }}</span>
          <span class="text-base font-extrabold">{{ day }}</span>
        </button>
      </div>
    </div>

    <div v-if="filteredEvents.length === 0" class="p-16 text-center text-slate-400 space-y-2 bg-white border border-slate-100 rounded-2xl">
      <i class="fa-regular fa-calendar-xmark text-3xl block mb-2"></i>
      <p class="text-sm font-semibold">선택한 날짜에 예정된 이벤트가 없습니다.</p>
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
      <div
        v-for="ev in filteredEvents"
        :key="ev.id"
        @click="openEventDetails(ev)"
        class="group bg-white rounded-2xl border border-slate-100 overflow-hidden hover:shadow-xl hover:border-blue-100 transition-all duration-300 cursor-pointer"
      >
        <div class="aspect-[3/4] bg-slate-100 relative overflow-hidden">
          <img :src="ev.img" :alt="ev.title" class="w-full h-full object-cover group-hover:scale-105 transition-all duration-500" />
          <span class="absolute top-3 left-3 px-2.5 py-1 bg-blue-600 text-white text-[10px] font-black rounded-lg shadow-sm">진행/예정</span>
        </div>
        <div class="p-4 space-y-1.5">
          <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded">{{ ev.category }}</span>
          <h3 class="text-sm font-black text-slate-800 group-hover:text-blue-600 transition truncate">{{ ev.title }}</h3>
          <p class="text-[11px] text-slate-400 font-semibold">{{ ev.dateStr }}</p>
        </div>
      </div>
    </div>

    <div class="text-center pt-2">
      <button @click="emit('open-calendar')" class="px-6 py-3 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-full text-xs font-black transition shadow-sm border border-blue-100/30">
        달력으로 전체 일정 보기 <i class="fa-solid fa-chevron-right ml-1"></i>
      </button>
    </div>
  </section>
</template>
