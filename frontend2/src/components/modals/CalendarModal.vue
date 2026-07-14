<script setup>
import { useEvents } from '../../composables/useEvents'

const emit = defineEmits(['close'])

const { selectedDate, getEventsForDate } = useEvents()
</script>

<template>
  <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[9999] flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-5xl overflow-hidden animate-fade-in flex flex-col max-h-[85vh]">
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center">
        <h3 class="text-lg font-black text-slate-900"><i class="fa-regular fa-calendar-days text-blue-600 mr-2"></i> 2026년 7월 종합 축제 & 행사 일정표</h3>
        <button @click="emit('close')" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark text-lg"></i></button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 overflow-y-auto">
        <div class="lg:col-span-7 p-6 border-r border-slate-100">
          <h4 class="text-base font-bold text-slate-800 mb-4 text-center">2026년 7월</h4>
          <div class="grid grid-cols-7 gap-1 text-center text-xs font-bold text-slate-400 mb-2">
            <div class="text-red-500">일</div>
            <div>월</div>
            <div>화</div>
            <div>수</div>
            <div>목</div>
            <div>금</div>
            <div class="text-blue-500">토</div>
          </div>
          <div class="grid grid-cols-7 gap-1.5">
            <div v-for="i in 3" :key="'blank-' + i" class="aspect-square bg-slate-50 rounded-lg opacity-30"></div>
            <button
              v-for="day in 31"
              :key="day"
              @click="selectedDate = `2026-07-${day.toString().padStart(2, '0')}`"
              :class="['aspect-square flex flex-col justify-between p-1.5 rounded-xl border transition', selectedDate === `2026-07-${day.toString().padStart(2, '0')}` ? 'bg-blue-600 border-blue-600 text-white font-bold' : 'bg-white border-slate-100 text-slate-800 hover:bg-slate-50']"
            >
              <span class="text-xs">{{ day }}</span>
              <span
                v-if="getEventsForDate(`2026-07-${day.toString().padStart(2, '0')}`).length > 0"
                class="w-1.5 h-1.5 rounded-full bg-orange-500 self-center"
              ></span>
            </button>
          </div>
        </div>

        <div class="lg:col-span-5 p-6 bg-slate-50/50 flex flex-col justify-between">
          <div>
            <span class="text-[10px] text-blue-600 font-extrabold block">SELECTED DATE EVENTS</span>
            <h4 class="text-2xl font-black text-slate-900 mb-4">{{ selectedDate.replace(/-/g, '.') }} 일자 일정</h4>

            <div class="space-y-2 max-h-[300px] overflow-y-auto custom-scrollbar">
              <div v-if="getEventsForDate(selectedDate).length === 0" class="text-center py-12 text-slate-400 text-xs">
                해당 날짜에 예정된 특별 행사가 없습니다.
              </div>
              <div v-else v-for="ev in getEventsForDate(selectedDate)" :key="ev.id" class="p-3 bg-white border border-slate-100 rounded-xl space-y-1">
                <span class="text-[10px] font-bold text-orange-600 bg-orange-50 px-2 py-0.5 rounded">{{ ev.category }}</span>
                <h5 class="text-xs font-extrabold text-slate-800">{{ ev.title }}</h5>
                <p class="text-[10px] text-slate-400 font-semibold">진행 기간: {{ ev.dateStr }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
