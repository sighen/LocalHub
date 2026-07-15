<script setup>
import { ref, onMounted } from 'vue'
import { useFestivals } from '../../composables/useFestivals'
import { useAppNavigation } from '../../composables/useAppNavigation'
import FestivalCalendar from './FestivalCalendar.vue'
import FestivalList from './FestivalList.vue'
import FestivalDetailModal from './FestivalDetailModal.vue'

const {
  year,
  month,
  monthLabel,
  selectedDate,
  district,
  viewMode,
  festivals,
  facets,
  isLoading,
  loadError,
  loadFestivals,
  loadFacets,
  goToMonth,
  selectDistrict,
  fetchFestivalDetail
} = useFestivals()

const { consumePlaceIntent, pushBack, popBack } = useAppNavigation()

const selectedContentId = ref(null)
const detailPlace = ref(null)
const isDetailLoading = ref(false)
const detailLoadError = ref(false)
let detailBackId = null

const openDetail = async (contentId) => {
  const openingFromList = selectedContentId.value === null
  if (openingFromList) detailBackId = pushBack(() => closeDetail())
  selectedContentId.value = contentId
  isDetailLoading.value = true
  detailLoadError.value = false
  try {
    const place = await fetchFestivalDetail(contentId)
    if (!place) {
      detailLoadError.value = true
      return
    }
    detailPlace.value = place
  } finally {
    isDetailLoading.value = false
  }
}

const retryDetail = () => {
  if (selectedContentId.value) openDetail(selectedContentId.value)
}

const closeDetail = () => {
  selectedContentId.value = null
  detailPlace.value = null
  if (detailBackId !== null) {
    popBack(detailBackId)
    detailBackId = null
  }
}

const retryList = () => {
  loadFestivals()
}

onMounted(async () => {
  await Promise.all([loadFacets(), loadFestivals()])

  const intent = consumePlaceIntent()
  if (intent?.contentTypeId === 15) {
    openDetail(intent.contentId)
  }
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8 animate-fade-in">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-6">
      <div>
        <h2 class="text-3xl font-black text-slate-900 tracking-tight">축제 · 공연 · 행사</h2>
        <p class="text-sm text-slate-500 mt-1">서울시 공공데이터 기반으로 진행 중이거나 예정된 축제·행사를 찾아보세요.</p>
      </div>

      <select
        :value="district"
        @change="selectDistrict($event.target.value)"
        class="px-3 py-2.5 text-xs font-bold bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 shrink-0"
      >
        <option value="">전체 권역</option>
        <option v-for="d in facets.districts" :key="d.value" :value="d.value">{{ d.value }} ({{ d.count }})</option>
      </select>
    </div>

    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-1.5">
        <button @click="goToMonth(-1)" class="p-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 transition"><i class="fa-solid fa-chevron-left"></i></button>
        <span class="text-base font-black text-slate-800 w-28 text-center">{{ monthLabel }}</span>
        <button @click="goToMonth(1)" class="p-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 transition"><i class="fa-solid fa-chevron-right"></i></button>
      </div>

      <div class="flex gap-1.5 bg-slate-100 p-1 rounded-xl w-fit">
        <button
          @click="viewMode = 'calendar'"
          :class="['px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5', viewMode === 'calendar' ? 'text-blue-600 bg-white shadow-sm' : 'text-slate-600 hover:text-slate-900']"
        >
          <i class="fa-regular fa-calendar-days"></i> 캘린더
        </button>
        <button
          @click="viewMode = 'list'"
          :class="['px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5', viewMode === 'list' ? 'text-blue-600 bg-white shadow-sm' : 'text-slate-600 hover:text-slate-900']"
        >
          <i class="fa-solid fa-list"></i> 목록
        </button>
      </div>
    </div>

    <FestivalCalendar
      v-if="viewMode === 'calendar'"
      :year="year"
      :month="month"
      :month-label="monthLabel"
      :selected-date="selectedDate"
      :festivals="festivals"
      :is-loading="isLoading"
      :load-error="loadError"
      @select-date="(d) => (selectedDate = d)"
      @open-detail="openDetail"
      @retry="retryList"
    />
    <FestivalList
      v-else
      :festivals="festivals"
      :is-loading="isLoading"
      :load-error="loadError"
      @open-detail="openDetail"
      @retry="retryList"
    />

    <FestivalDetailModal
      v-if="selectedContentId"
      :place="detailPlace"
      :is-loading="isDetailLoading"
      :load-error="detailLoadError"
      @close="closeDetail"
      @retry="retryDetail"
    />
  </div>
</template>
