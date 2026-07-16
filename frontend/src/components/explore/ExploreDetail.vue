<script setup>
import { ref, watch } from 'vue'
import ExploreMap from './ExploreMap.vue'
import NearbyPlaceModal from './NearbyPlaceModal.vue'
import client from '../../api/client'
import { useWeather } from '../../composables/useWeather'
import { useAppNavigation } from '../../composables/useAppNavigation'
import { tagLabel } from '../../utils/tagLabels'
import { secureImageUrl } from '../../utils/imageUrl'
import { resolvePlaceImage } from '../../utils/placeImage'
import defaultPlace from '../../assets/default-place.svg'

const props = defineProps({
  place: { type: Object, default: null },
  nearby: { type: Object, default: () => ({ festival: null, attraction: null }) },
  isLoading: { type: Boolean, default: false },
  loadError: { type: Boolean, default: false }
})

const emit = defineEmits(['back', 'retry'])

const { weatherData } = useWeather()
const { requestWriteReview, requestViewReviews } = useAppNavigation()

const nearbyModalPlace = ref(null)

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
</script>

<template>
  <div class="space-y-5">
    <button @click="emit('back')" class="flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-slate-800 transition">
      <i class="fa-solid fa-arrow-left"></i> 목록으로
    </button>

    <div v-if="isLoading" class="p-16 text-center text-slate-400 space-y-2">
      <i class="fa-solid fa-spinner fa-spin text-3xl block mb-2"></i>
      <p class="text-sm font-semibold">불러오는 중입니다...</p>
    </div>

    <div v-else-if="loadError || !place" class="p-16 text-center text-slate-400 space-y-3">
      <i class="fa-solid fa-triangle-exclamation text-4xl block mb-2 text-amber-400"></i>
      <p class="text-sm font-semibold text-slate-500">상세 정보를 불러오지 못했어요. 잠시 후 다시 시도해주세요.</p>
      <button @click="emit('retry')" class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-700 transition">다시 시도</button>
    </div>

    <template v-else>
      <div class="bg-white border border-slate-100 rounded-3xl shadow-sm overflow-hidden">
        <div v-if="place.image_url" class="h-64 bg-slate-100 overflow-hidden">
          <img :src="secureImageUrl(place.image_url) || defaultPlace" :alt="place.title" class="w-full h-full object-cover" @error="(e) => { e.target.src = defaultPlace }" />
        </div>

        <div class="p-6 space-y-4">
          <div class="flex items-center justify-between gap-3 flex-wrap">
            <div class="flex items-center gap-2 text-xs">
              <span v-if="place.district_name" class="px-2.5 py-1 bg-blue-50 text-blue-600 font-extrabold rounded-lg border border-blue-100">{{ place.district_name }}</span>
              <span v-if="place.category_l1" class="px-2.5 py-1 bg-slate-100 text-slate-500 font-extrabold rounded-lg">{{ tagLabel(place.category_l1) }}</span>
            </div>
            <div class="flex items-center gap-1.5 px-3 py-1.5 bg-sky-50 border border-sky-100 rounded-xl text-sky-700 text-xs font-bold">
              <span>{{ weatherData.icon }}</span>
              <span>서울 {{ weatherData.temp }}°C · {{ weatherData.status }}</span>
            </div>
          </div>

          <h2 class="text-2xl font-black text-slate-900 leading-tight">{{ place.title }}</h2>

          <div class="space-y-1.5 text-xs text-slate-500">
            <p v-if="place.addr1"><i class="fa-solid fa-location-dot w-4 text-slate-400"></i> {{ place.addr1 }} {{ place.addr2 }}</p>
            <p v-if="place.tel"><i class="fa-solid fa-phone w-4 text-slate-400"></i> {{ place.tel }}</p>
            <p v-if="place.homepage_url">
              <i class="fa-solid fa-globe w-4 text-slate-400"></i>
              <a :href="place.homepage_url" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">{{ place.homepage_url }}</a>
            </p>
          </div>

          <p v-if="place.overview" class="text-xs text-slate-600 leading-relaxed whitespace-pre-line border-t border-slate-100 pt-4">{{ place.overview }}</p>
        </div>
      </div>

      <div class="bg-white border border-slate-100 rounded-3xl shadow-sm p-5 flex items-center justify-between gap-3 flex-wrap">
        <span class="text-xs font-bold text-slate-600"><i class="fa-regular fa-comment-dots mr-1.5 text-slate-400"></i>커뮤니티 후기 {{ reviewCount }}개</span>
        <div class="flex gap-2">
          <button @click="requestViewReviews(place)" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition">리뷰 보기</button>
          <button @click="requestWriteReview(place)" class="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg transition">이 장소 리뷰 쓰기</button>
        </div>
      </div>

      <div class="bg-white border border-slate-100 rounded-3xl shadow-sm p-6 space-y-3">
        <h3 class="text-sm font-black text-slate-800">위치</h3>
        <ExploreMap v-if="place.latitude && place.longitude" :places="[place]" height="h-72" />
        <p v-else class="text-xs text-slate-400">좌표 정보가 없어 지도를 표시할 수 없습니다.</p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div class="bg-white border border-slate-100 rounded-3xl shadow-sm p-5 space-y-3">
          <h3 class="text-sm font-black text-slate-800"><i class="fa-solid fa-champagne-glasses text-orange-500 mr-1.5"></i>근처 축제행사</h3>
          <div v-if="!nearby.festival" class="text-[11px] text-slate-300 py-6 text-center">
            근처에 진행 중인 축제행사가 없습니다.
          </div>
          <div
            v-else
            @click="nearbyModalPlace = nearby.festival"
            class="flex items-center gap-3 bg-slate-50 rounded-xl px-3.5 py-2.5 cursor-pointer hover:bg-slate-100 transition"
          >
            <img
              :src="secureImageUrl(resolvePlaceImage(nearby.festival)) || defaultPlace"
              :alt="nearby.festival.title"
              class="w-12 h-12 rounded-lg object-cover flex-shrink-0"
              @error="(e) => { e.target.src = defaultPlace }"
            />
            <p class="text-xs font-bold text-slate-700 truncate">{{ nearby.festival.title }}</p>
          </div>
        </div>

        <div class="bg-white border border-slate-100 rounded-3xl shadow-sm p-5 space-y-3">
          <h3 class="text-sm font-black text-slate-800"><i class="fa-solid fa-map-location-dot text-indigo-500 mr-1.5"></i>근처 관광지 추천</h3>
          <div v-if="!nearby.attraction" class="text-[11px] text-slate-300 py-6 text-center">
            근처에 추천할 관광지가 없습니다.
          </div>
          <div
            v-else
            @click="nearbyModalPlace = nearby.attraction"
            class="flex items-center gap-3 bg-slate-50 rounded-xl px-3.5 py-2.5 cursor-pointer hover:bg-slate-100 transition"
          >
            <img
              :src="secureImageUrl(resolvePlaceImage(nearby.attraction)) || defaultPlace"
              :alt="nearby.attraction.title"
              class="w-12 h-12 rounded-lg object-cover flex-shrink-0"
              @error="(e) => { e.target.src = defaultPlace }"
            />
            <p class="text-xs font-bold text-slate-700 truncate">{{ nearby.attraction.title }}</p>
          </div>
        </div>
      </div>
    </template>

    <NearbyPlaceModal :place="nearbyModalPlace" @close="nearbyModalPlace = null" />
  </div>
</template>
