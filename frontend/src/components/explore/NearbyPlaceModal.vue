<script setup>
import { ref, watch } from 'vue'
import ExploreMap from './ExploreMap.vue'
import client from '../../api/client'
import { formatEventPeriod } from '../../composables/useFestivals'
import { useAppNavigation } from '../../composables/useAppNavigation'
import { tagLabel } from '../../utils/tagLabels'
import { secureImageUrl } from '../../utils/imageUrl'
import { resolvePlaceImage } from '../../utils/placeImage'
import defaultPlace from '../../assets/default-place.svg'

const props = defineProps({
  place: { type: Object, default: null }
})

const emit = defineEmits(['close'])

const { requestWriteReview, requestViewReviews } = useAppNavigation()

const reviewCount = ref(0)

const loadReviewCount = async () => {
  if (!props.place) return
  try {
    const { data } = await client.get('/posts', { params: { place_content_id: props.place.content_id, size: 1 } })
    reviewCount.value = data.total
  } catch (e) {
    reviewCount.value = 0
  }
}

watch(() => props.place, (place) => { if (place) loadReviewCount() }, { immediate: true })

const isFestival = (place) => place.content_type_id === 15
</script>

<template>
  <Teleport to="body">
    <div v-if="place" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[9999] flex items-center justify-center p-4" @click.self="emit('close')">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-xl overflow-hidden animate-fade-in flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center shrink-0">
          <span
            class="px-2.5 py-1 text-xs font-bold rounded-lg border"
            :class="isFestival(place) ? 'bg-orange-50 text-orange-600 border-orange-100' : 'bg-blue-50 text-blue-600 border-blue-100'"
          >{{ isFestival(place) ? '축제·행사' : (tagLabel(place.category_l1) || '관광 추천') }}</span>
          <button @click="emit('close')" class="p-1.5 text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
        </div>

        <div class="p-6 space-y-5 overflow-y-auto">
          <div v-if="resolvePlaceImage(place)" class="h-48 rounded-xl overflow-hidden border border-slate-200">
            <img :src="secureImageUrl(resolvePlaceImage(place)) || defaultPlace" :alt="place.title" class="w-full h-full object-cover" @error="(e) => { e.target.src = defaultPlace }" />
          </div>

          <div class="space-y-1.5">
            <h3 class="text-xl font-black text-slate-900 leading-tight">{{ place.title }}</h3>
            <div class="flex items-center gap-2 text-xs text-slate-400">
              <span v-if="place.district_name">{{ place.district_name }}</span>
            </div>
          </div>

          <div class="space-y-1.5 text-xs text-slate-500 border-t border-slate-100 pt-4">
            <p v-if="isFestival(place)"><i class="fa-regular fa-calendar w-4 text-slate-400"></i> 기간: {{ formatEventPeriod(place.event_start_date, place.event_end_date) }}</p>
            <p v-if="place.addr1"><i class="fa-solid fa-location-dot w-4 text-slate-400"></i> {{ place.addr1 }} {{ place.addr2 }}</p>
            <p v-if="place.tel"><i class="fa-solid fa-phone w-4 text-slate-400"></i> {{ place.tel }}</p>
            <p v-if="place.homepage_url">
              <i class="fa-solid fa-globe w-4 text-slate-400"></i>
              <a :href="place.homepage_url" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">{{ place.homepage_url }}</a>
            </p>
          </div>

          <p v-if="place.overview" class="text-xs text-slate-600 leading-relaxed whitespace-pre-line">{{ place.overview }}</p>

          <div v-if="place.latitude && place.longitude" class="space-y-2">
            <h4 class="text-xs font-black text-slate-700">위치</h4>
            <ExploreMap :places="[place]" height="h-56" />
          </div>

          <div class="border-t border-slate-100 pt-4 flex items-center justify-between gap-3 flex-wrap">
            <span class="text-xs font-bold text-slate-600"><i class="fa-regular fa-comment-dots mr-1.5 text-slate-400"></i>커뮤니티 후기 {{ reviewCount }}개</span>
            <div class="flex gap-2">
              <button @click="requestViewReviews(place)" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition">리뷰 보기</button>
              <button @click="requestWriteReview(place)" class="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg transition">이 장소 리뷰 쓰기</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
