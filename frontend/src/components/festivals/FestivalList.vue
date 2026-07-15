<script setup>
import { formatEventPeriod } from '../../composables/useFestivals'
import { secureImageUrl } from '../../utils/imageUrl'
import { resolvePlaceImage } from '../../utils/placeImage'

defineProps({
  festivals: { type: Array, required: true },
  isLoading: { type: Boolean, default: false },
  loadError: { type: Boolean, default: false }
})

const emit = defineEmits(['open-detail', 'retry'])
</script>

<template>
  <div>
    <div v-if="isLoading" class="p-16 text-center text-slate-400 space-y-2 bg-white border border-slate-100 rounded-3xl shadow-sm">
      <i class="fa-solid fa-spinner fa-spin text-3xl block mb-2"></i>
      <p class="text-sm font-semibold">불러오는 중입니다...</p>
    </div>

    <div v-else-if="loadError" class="p-16 text-center text-slate-400 space-y-3 bg-white border border-slate-100 rounded-3xl shadow-sm">
      <i class="fa-solid fa-triangle-exclamation text-4xl block mb-2 text-amber-400"></i>
      <p class="text-sm font-semibold text-slate-500">목록을 불러오지 못했어요. 잠시 후 다시 시도해주세요.</p>
      <button @click="emit('retry')" class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-700 transition">다시 시도</button>
    </div>

    <div v-else-if="festivals.length === 0" class="p-16 text-center text-slate-400 space-y-2 bg-white border border-slate-100 rounded-3xl shadow-sm">
      <i class="fa-regular fa-calendar-xmark text-4xl block mb-2"></i>
      <p class="text-sm font-semibold">이번 달 예정된 축제·행사가 없습니다.</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-10">
      <div
        v-for="f in festivals"
        :key="f.content_id"
        @click="emit('open-detail', f.content_id)"
        class="flip-card aspect-[4/5] max-w-[280px] mx-auto w-full cursor-pointer"
      >
        <div class="flip-card-inner">
          <div class="flip-card-front rounded-2xl border border-slate-100 shadow-sm overflow-hidden bg-slate-100">
            <template v-if="resolvePlaceImage(f)">
              <img
                :src="secureImageUrl(resolvePlaceImage(f))"
                :alt="f.title"
                loading="lazy"
                class="w-full h-full object-cover"
              />
            </template>
            <template v-else>
              <div class="w-full h-full bg-slate-200"></div>
            </template>
            <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent p-4 space-y-1">
              <span v-if="f.district_name" class="text-[10px] font-bold text-white bg-white/20 px-2 py-0.5 rounded backdrop-blur-sm">{{ f.district_name }}</span>
              <h3 class="text-sm font-black text-white truncate">{{ f.title }}</h3>
            </div>
          </div>

          <div class="flip-card-back rounded-2xl border border-slate-100 shadow-sm bg-white p-5 flex flex-col">
            <span v-if="f.district_name" class="text-[10px] font-bold text-orange-600 bg-orange-50 px-2 py-0.5 rounded w-fit">{{ f.district_name }}</span>
            <h3 class="text-sm font-black text-slate-800 mt-2 leading-snug">{{ f.title }}</h3>
            <p class="text-[11px] text-slate-400 font-semibold mt-1">
              <i class="fa-regular fa-calendar mr-1"></i>{{ formatEventPeriod(f.event_start_date, f.event_end_date) }}
            </p>
            <p v-if="f.addr1" class="text-[11px] text-slate-400 mt-1 truncate">
              <i class="fa-solid fa-location-dot mr-1"></i>{{ f.addr1 }}
            </p>
            <p v-if="f.overview" class="text-[11px] text-slate-500 leading-relaxed line-clamp-4 mt-3">{{ f.overview }}</p>
            <span class="mt-auto pt-2 text-[10px] font-bold text-blue-600">자세히 보기 <i class="fa-solid fa-arrow-right ml-0.5"></i></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.flip-card {
  perspective: 1200px;
  position: relative;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}
.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}
.flip-card-front,
.flip-card-back {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}
.flip-card-back {
  transform: rotateY(180deg);
}
</style>
