<script setup>
import { tagLabel } from '../../utils/tagLabels'
import { secureImageUrl } from '../../utils/imageUrl'
import { resolvePlaceImage, resolvePlaceImageCandidates } from '../../utils/placeImage'

const props = defineProps({
  places: { type: Array, required: true },
  isLoading: { type: Boolean, default: false },
  loadError: { type: Boolean, default: false },
  page: { type: Number, required: true },
  total: { type: Number, required: true },
  pageSize: { type: Number, required: true }
})

const emit = defineEmits(['open-detail', 'retry', 'go-to-page'])

const totalPages = () => Math.max(1, Math.ceil(props.total / props.pageSize))

// A place can have multiple candidate image URLs (e.g. image_url, thumbnail_url)
// and any one of them may be a dead link on the upstream CDN, so on error we
// try the next candidate before finally falling back to the placeholder.
function onImageError(event, place) {
  const candidates = resolvePlaceImageCandidates(place).map((c) => secureImageUrl(c) || c)
  const nextIndex = Number(event.target.dataset.fallbackIndex || 0) + 1
  if (nextIndex < candidates.length) {
    event.target.dataset.fallbackIndex = nextIndex
    event.target.src = candidates[nextIndex]
  }
}
</script>

<template>
  <div>
    <div v-if="isLoading" class="p-16 text-center text-slate-400 space-y-2">
      <i class="fa-solid fa-spinner fa-spin text-3xl block mb-2"></i>
      <p class="text-sm font-semibold">불러오는 중입니다...</p>
    </div>

    <div v-else-if="loadError" class="p-16 text-center text-slate-400 space-y-3">
      <i class="fa-solid fa-triangle-exclamation text-4xl block mb-2 text-amber-400"></i>
      <p class="text-sm font-semibold text-slate-500">목록을 불러오지 못했어요. 잠시 후 다시 시도해주세요.</p>
      <button @click="emit('retry')" class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-700 transition">다시 시도</button>
    </div>

    <div v-else-if="places.length === 0" class="p-16 text-center text-slate-400 space-y-2">
      <i class="fa-regular fa-folder-open text-4xl block mb-2"></i>
      <p class="text-sm font-semibold">아직 준비된 데이터가 없습니다.</p>
      <p class="text-xs text-slate-300">다른 카테고리나 필터를 선택해보세요.</p>
    </div>

    <template v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
        <div
          v-for="place in places"
          :key="place.content_id"
          @click="emit('open-detail', place.content_id)"
          class="group bg-white rounded-2xl border border-slate-100 overflow-hidden hover:shadow-lg hover:border-blue-100 transition duration-300 cursor-pointer"
        >
          <div class="h-40 bg-slate-100 overflow-hidden relative">
            <template v-if="resolvePlaceImage(place)">
              <img
                :src="secureImageUrl(resolvePlaceImage(place))"
                :alt="place.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-all duration-500"
                @error="(e) => onImageError(e, place)"
              />
            </template>
            <template v-else>
              <div class="w-full h-full bg-slate-200"></div>
            </template>
          </div>
          <div class="p-4 space-y-1.5">
            <div class="flex items-center gap-1.5 text-[10px]">
              <span v-if="place.district_name" class="px-2 py-0.5 bg-blue-50 text-blue-600 font-extrabold rounded">{{ place.district_name }}</span>
              <span v-if="place.category_l1" class="px-2 py-0.5 bg-slate-100 text-slate-500 font-extrabold rounded">{{ tagLabel(place.category_l1) }}</span>
            </div>
            <h3 class="text-sm font-extrabold text-slate-800 group-hover:text-blue-600 transition truncate">{{ place.title }}</h3>
            <p class="text-[11px] text-slate-400 truncate">{{ place.addr1 }}</p>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-center gap-3 pt-8">
        <button
          :disabled="page <= 1"
          @click="emit('go-to-page', page - 1)"
          class="px-3 py-1.5 text-xs font-bold rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition disabled:opacity-40 disabled:cursor-not-allowed"
        >
          이전
        </button>
        <span class="text-xs font-bold text-slate-500">{{ page }} / {{ totalPages() }}</span>
        <button
          :disabled="page >= totalPages()"
          @click="emit('go-to-page', page + 1)"
          class="px-3 py-1.5 text-xs font-bold rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition disabled:opacity-40 disabled:cursor-not-allowed"
        >
          다음
        </button>
      </div>
    </template>
  </div>
</template>
