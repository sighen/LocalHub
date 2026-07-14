<script setup>
import { formatEventPeriod } from '../../composables/useFestivals'

defineProps({
  festivals: { type: Array, required: true },
  isLoading: { type: Boolean, default: false },
  loadError: { type: Boolean, default: false }
})

const emit = defineEmits(['open-detail', 'retry'])
</script>

<template>
  <div class="bg-white border border-slate-100 rounded-3xl shadow-sm overflow-hidden">
    <div v-if="isLoading" class="p-16 text-center text-slate-400 space-y-2">
      <i class="fa-solid fa-spinner fa-spin text-3xl block mb-2"></i>
      <p class="text-sm font-semibold">불러오는 중입니다...</p>
    </div>

    <div v-else-if="loadError" class="p-16 text-center text-slate-400 space-y-3">
      <i class="fa-solid fa-triangle-exclamation text-4xl block mb-2 text-amber-400"></i>
      <p class="text-sm font-semibold text-slate-500">목록을 불러오지 못했어요. 잠시 후 다시 시도해주세요.</p>
      <button @click="emit('retry')" class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-700 transition">다시 시도</button>
    </div>

    <div v-else-if="festivals.length === 0" class="p-16 text-center text-slate-400 space-y-2">
      <i class="fa-regular fa-calendar-xmark text-4xl block mb-2"></i>
      <p class="text-sm font-semibold">이번 달 예정된 축제·행사가 없습니다.</p>
    </div>

    <div v-else class="divide-y divide-slate-100">
      <div
        v-for="f in festivals"
        :key="f.content_id"
        @click="emit('open-detail', f.content_id)"
        class="p-5 hover:bg-slate-50/50 cursor-pointer transition flex gap-4 items-center"
      >
        <div class="w-20 h-20 rounded-xl bg-slate-100 overflow-hidden shrink-0">
          <img v-if="f.thumbnail_url" :src="f.thumbnail_url" :alt="f.title" class="w-full h-full object-cover" />
          <div v-else class="w-full h-full flex items-center justify-center text-slate-300">
            <i class="fa-regular fa-image text-xl"></i>
          </div>
        </div>
        <div class="space-y-1 flex-grow min-w-0">
          <span v-if="f.district_name" class="text-[10px] font-bold text-orange-600 bg-orange-50 px-2 py-0.5 rounded">{{ f.district_name }}</span>
          <h3 class="text-sm font-black text-slate-800 truncate">{{ f.title }}</h3>
          <p class="text-[11px] text-slate-400 font-semibold">{{ formatEventPeriod(f.event_start_date, f.event_end_date) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
