<script setup>
import { ref, onMounted } from 'vue'
import { useLocations } from '../../composables/useLocations'
import ExploreFilters from './ExploreFilters.vue'
import ExploreDistrictMap from './ExploreDistrictMap.vue'
import ExploreList from './ExploreList.vue'
import ExploreMap from './ExploreMap.vue'
import ExploreDetail from './ExploreDetail.vue'

const props = defineProps({
  initialCategory: { type: String, default: '관광지' },
  initialTag: { type: String, default: '' }
})

const {
  activeCategory,
  districts,
  tag,
  sort,
  viewMode,
  places,
  page,
  total,
  pageSize,
  mapPoints,
  isMapLoading,
  mapLoadError,
  facets,
  isLoading,
  loadError,
  loadPlaces,
  loadMapPoints,
  loadFacets,
  setCategory,
  applyFilters,
  toggleDistrict,
  clearDistricts,
  goToPage,
  fetchPlaceDetail,
  fetchNearby
} = useLocations()

const CATEGORIES = ['관광지', '문화시설', '레포츠']

const selectedContentId = ref(null)
const detailPlace = ref(null)
const detailNearby = ref({ restaurants: [], lodgings: [] })
const isDetailLoading = ref(false)
const detailLoadError = ref(false)

const openDetail = async (contentId) => {
  selectedContentId.value = contentId
  isDetailLoading.value = true
  detailLoadError.value = false
  try {
    const [place, nearby] = await Promise.all([fetchPlaceDetail(contentId), fetchNearby(contentId)])
    if (!place) {
      detailLoadError.value = true
      return
    }
    detailPlace.value = place
    detailNearby.value = nearby
  } finally {
    isDetailLoading.value = false
  }
}

const retryDetail = () => {
  if (selectedContentId.value) openDetail(selectedContentId.value)
}

const backToList = () => {
  selectedContentId.value = null
  detailPlace.value = null
}

const onSelectTag = (value) => {
  tag.value = value
  applyFilters()
}

const onSelectSort = (value) => {
  sort.value = value
  applyFilters()
}

const onSelectMapPlace = (contentId) => {
  openDetail(contentId)
}

const retryList = () => {
  loadPlaces()
}

onMounted(() => {
  activeCategory.value = props.initialCategory
  tag.value = props.initialTag
  loadFacets()
  loadPlaces()
  loadMapPoints()
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8 animate-fade-in">
    <template v-if="selectedContentId">
      <ExploreDetail
        :place="detailPlace"
        :nearby="detailNearby"
        :is-loading="isDetailLoading"
        :load-error="detailLoadError"
        @back="backToList"
        @retry="retryDetail"
      />
    </template>

    <template v-else>
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <h2 class="text-3xl font-black text-slate-900 tracking-tight">관광지 · 문화시설 · 레포츠 추천</h2>
          <p class="text-sm text-slate-500 mt-1">서울시 공공데이터 기반으로 관심 있는 장소를 찾아보세요.</p>
        </div>

        <div v-if="districts.length" class="text-xs font-bold text-blue-600 bg-blue-50 border border-blue-100 rounded-xl px-3 py-2 shrink-0">
          선택된 권역: {{ districts.join(', ') }}
        </div>
      </div>

      <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex gap-1.5 bg-slate-100 p-1 rounded-xl w-fit">
          <button
            v-for="c in CATEGORIES"
            :key="c"
            @click="setCategory(c)"
            :class="['px-4 py-2 text-sm font-semibold rounded-lg transition-all', activeCategory === c ? 'text-blue-600 bg-white shadow-sm' : 'text-slate-600 hover:text-slate-900']"
          >
            {{ c }}
          </button>
        </div>

        <div class="flex gap-1.5 bg-slate-100 p-1 rounded-xl w-fit">
          <button
            @click="viewMode = 'list'"
            :class="['px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5', viewMode === 'list' ? 'text-blue-600 bg-white shadow-sm' : 'text-slate-600 hover:text-slate-900']"
          >
            <i class="fa-solid fa-list"></i> 목록
          </button>
          <button
            @click="viewMode = 'map'"
            :class="['px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5', viewMode === 'map' ? 'text-blue-600 bg-white shadow-sm' : 'text-slate-600 hover:text-slate-900']"
          >
            <i class="fa-solid fa-map"></i> 지도
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-[440px_1fr] gap-6 items-start">
        <div class="space-y-4">
          <ExploreDistrictMap :districts="districts" @toggle-district="toggleDistrict" @clear-districts="clearDistricts" />
          <ExploreFilters
            :tag="tag"
            :sort="sort"
            :facets="facets"
            @select-tag="onSelectTag"
            @select-sort="onSelectSort"
          />
        </div>

        <div v-if="viewMode === 'map'">
          <div v-if="isMapLoading" class="p-16 text-center text-slate-400 space-y-2">
            <i class="fa-solid fa-spinner fa-spin text-3xl block mb-2"></i>
            <p class="text-sm font-semibold">지도를 불러오는 중입니다...</p>
          </div>
          <div v-else-if="mapLoadError" class="p-16 text-center text-slate-400 space-y-3">
            <i class="fa-solid fa-triangle-exclamation text-4xl block mb-2 text-amber-400"></i>
            <p class="text-sm font-semibold text-slate-500">지도를 불러오지 못했어요. 잠시 후 다시 시도해주세요.</p>
            <button @click="loadMapPoints" class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-700 transition">다시 시도</button>
          </div>
          <template v-else>
            <p class="text-xs text-slate-400 mb-2">총 {{ mapPoints.length }}곳이 지도에 표시됩니다.</p>
            <ExploreMap :places="mapPoints" @select-place="onSelectMapPlace" />
          </template>
        </div>
        <div v-else>
          <ExploreList
            :places="places"
            :is-loading="isLoading"
            :load-error="loadError"
            :page="page"
            :total="total"
            :page-size="pageSize"
            @open-detail="openDetail"
            @retry="retryList"
            @go-to-page="goToPage"
          />
        </div>
      </div>
    </template>
  </div>
</template>
