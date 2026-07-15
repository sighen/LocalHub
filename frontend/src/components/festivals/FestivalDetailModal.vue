<script setup>
import ExploreMap from '../explore/ExploreMap.vue'
import { formatEventPeriod } from '../../composables/useFestivals'
import { secureImageUrl } from '../../utils/imageUrl'

defineProps({
  place: { type: Object, default: null },
  relatedPosts: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
  loadError: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'retry', 'open-post'])
</script>

<template>
  <Teleport to="body">
  <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[9999] flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-xl overflow-hidden animate-fade-in flex flex-col max-h-[90vh]">
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center shrink-0">
        <span class="px-2.5 py-1 bg-orange-50 text-orange-600 text-xs font-bold rounded-lg border border-orange-100">축제·행사</span>
        <button @click="emit('close')" class="p-1.5 text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <div class="p-6 space-y-5 overflow-y-auto">
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
          <div v-if="place.image_url" class="h-48 rounded-xl overflow-hidden border border-slate-200">
            <img :src="secureImageUrl(place.image_url)" :alt="place.title" class="w-full h-full object-cover" />
          </div>

          <div class="space-y-1.5">
            <h3 class="text-xl font-black text-slate-900 leading-tight">{{ place.title }}</h3>
            <div class="flex items-center gap-2 text-xs text-slate-400">
              <span v-if="place.district_name">{{ place.district_name }}</span>
            </div>
          </div>

          <div class="space-y-1.5 text-xs text-slate-500 border-t border-slate-100 pt-4">
            <p><i class="fa-regular fa-calendar w-4 text-slate-400"></i> 기간: {{ formatEventPeriod(place.event_start_date, place.event_end_date) }}</p>
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

          <div class="border-t border-slate-100 pt-4 space-y-2">
            <h4 class="text-xs font-black text-slate-700">관련 커뮤니티 게시글</h4>
            <div v-if="relatedPosts.length === 0" class="text-[11px] text-slate-300 py-4 text-center">
              관련된 커뮤니티 게시글이 없습니다.
            </div>
            <div v-else class="space-y-2">
              <div
                v-for="post in relatedPosts"
                :key="post.id"
                @click="emit('open-post', post.id)"
                class="bg-slate-50 rounded-xl px-3.5 py-2.5 cursor-pointer hover:bg-slate-100 transition"
              >
                <p class="text-xs font-bold text-slate-700 truncate">{{ post.title }}</p>
                <p class="text-[10px] text-slate-400">댓글 {{ post.comment_count }}개 · 조회 {{ post.view_count }}</p>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
  </Teleport>
</template>
