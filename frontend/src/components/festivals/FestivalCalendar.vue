<script setup>
import { computed } from 'vue'
import { formatEventDate } from '../../composables/useFestivals'

const props = defineProps({
  year: { type: Number, required: true },
  month: { type: Number, required: true },
  monthLabel: { type: String, required: true },
  selectedDate: { type: String, required: true },
  festivals: { type: Array, required: true },
  isLoading: { type: Boolean, default: false },
  loadError: { type: Boolean, default: false }
})

const emit = defineEmits(['select-date', 'open-detail', 'retry'])

const pad2 = (n) => String(n).padStart(2, '0')

const leadingBlanks = computed(() => new Date(props.year, props.month - 1, 1).getDay())
const daysInMonth = computed(() => new Date(props.year, props.month, 0).getDate())

const dateStrFor = (day) => `${props.year}-${pad2(props.month)}-${pad2(day)}`

const hasFestivalOn = (day) => {
  const compact = dateStrFor(day).replace(/-/g, '')
  return props.festivals.some(
    (f) => f.event_start_date && f.event_end_date && f.event_start_date <= compact && f.event_end_date >= compact
  )
}

const festivalsForSelectedDate = computed(() => {
  const compact = props.selectedDate.replace(/-/g, '')
  return props.festivals.filter(
    (f) => f.event_start_date && f.event_end_date && f.event_start_date <= compact && f.event_end_date >= compact
  )
})
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
    <div class="lg:col-span-7 bg-white border border-slate-100 rounded-3xl shadow-sm p-6">
      <div class="flex items-center justify-center mb-4">
        <h4 class="text-base font-black text-slate-800">{{ monthLabel }}</h4>
      </div>

      <div v-if="isLoading" class="p-16 text-center text-slate-400">
        <i class="fa-solid fa-spinner fa-spin text-3xl block mb-2"></i>
      </div>
      <div v-else-if="loadError" class="p-16 text-center text-slate-400 space-y-3">
        <i class="fa-solid fa-triangle-exclamation text-4xl block mb-2 text-amber-400"></i>
        <p class="text-sm font-semibold text-slate-500">일정을 불러오지 못했어요. 잠시 후 다시 시도해주세요.</p>
        <button @click="emit('retry')" class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-700 transition">다시 시도</button>
      </div>
      <template v-else>
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
          <div v-for="i in leadingBlanks" :key="'blank-' + i" class="aspect-square bg-slate-50 rounded-lg opacity-30"></div>
          <button
            v-for="day in daysInMonth"
            :key="day"
            @click="emit('select-date', dateStrFor(day))"
            :class="['aspect-square flex flex-col justify-between p-1.5 rounded-xl border transition', selectedDate === dateStrFor(day) ? 'bg-blue-600 border-blue-600 text-white font-bold' : 'bg-white border-slate-100 text-slate-800 hover:bg-slate-50']"
          >
            <span class="text-xs">{{ day }}</span>
            <span v-if="hasFestivalOn(day)" class="w-1.5 h-1.5 rounded-full bg-orange-500 self-center"></span>
          </button>
        </div>
      </template>
    </div>

    <div class="lg:col-span-5 bg-slate-50/50 border border-slate-100 rounded-3xl p-6 flex flex-col">
      <span class="text-[10px] text-blue-600 font-extrabold block">SELECTED DATE</span>
      <h4 class="text-2xl font-black text-slate-900 mb-4">{{ selectedDate.replace(/-/g, '.') }}</h4>

      <div class="space-y-2 max-h-[360px] overflow-y-auto custom-scrollbar">
        <div v-if="festivalsForSelectedDate.length === 0" class="text-center py-12 text-slate-400 text-xs">
          해당 날짜에 예정된 축제·행사가 없습니다.
        </div>
        <div
          v-else
          v-for="f in festivalsForSelectedDate"
          :key="f.content_id"
          @click="emit('open-detail', f.content_id)"
          class="p-3 bg-white border border-slate-100 rounded-xl space-y-1 cursor-pointer hover:border-blue-200 hover:shadow-sm transition"
        >
          <span v-if="f.district_name" class="text-[10px] font-bold text-orange-600 bg-orange-50 px-2 py-0.5 rounded">{{ f.district_name }}</span>
          <h5 class="text-xs font-extrabold text-slate-800">{{ f.title }}</h5>
          <p class="text-[10px] text-slate-400 font-semibold">{{ formatEventDate(f.event_start_date) }} ~ {{ formatEventDate(f.event_end_date) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
