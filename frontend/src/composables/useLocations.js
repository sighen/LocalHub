import { ref } from 'vue'
import client from '../api/client'

const PAGE_SIZE = 24

export function useLocations() {
  const activeCategory = ref('관광지')
  const districts = ref([])
  const tag = ref('')
  const sort = ref('title')
  const keyword = ref('')
  const viewMode = ref('list')

  const places = ref([])
  const page = ref(1)
  const total = ref(0)

  const mapPoints = ref([])
  const isMapLoading = ref(false)
  const mapLoadError = ref(false)

  const facets = ref({ districts: [], tags: [] })

  const isLoading = ref(false)
  const loadError = ref(false)
  const isFacetsLoading = ref(false)

  const loadPlaces = async () => {
    isLoading.value = true
    loadError.value = false
    try {
      const { data } = await client.get('/locations', {
        params: {
          type: activeCategory.value,
          district: districts.value.length ? districts.value : undefined,
          tag: tag.value || undefined,
          sort: sort.value,
          q: keyword.value || undefined,
          page: page.value,
          size: PAGE_SIZE
        }
      })
      places.value = data.items
      total.value = data.total
    } catch (e) {
      loadError.value = true
      places.value = []
      total.value = 0
    } finally {
      isLoading.value = false
    }
  }

  const loadMapPoints = async () => {
    isMapLoading.value = true
    mapLoadError.value = false
    try {
      const { data } = await client.get('/locations/points', {
        params: {
          type: activeCategory.value,
          district: districts.value.length ? districts.value : undefined,
          tag: tag.value || undefined,
          q: keyword.value || undefined
        }
      })
      mapPoints.value = data
    } catch (e) {
      mapLoadError.value = true
      mapPoints.value = []
    } finally {
      isMapLoading.value = false
    }
  }

  const loadFacets = async () => {
    isFacetsLoading.value = true
    try {
      const { data } = await client.get('/locations/facets', {
        params: { type: activeCategory.value }
      })
      facets.value = data
    } catch (e) {
      facets.value = { districts: [], tags: [] }
    } finally {
      isFacetsLoading.value = false
    }
  }

  const setCategory = (category) => {
    activeCategory.value = category
    districts.value = []
    tag.value = ''
    page.value = 1
    loadFacets()
    loadPlaces()
    loadMapPoints()
  }

  const applyFilters = () => {
    page.value = 1
    loadPlaces()
    loadMapPoints()
  }

  const toggleDistrict = (value) => {
    const idx = districts.value.indexOf(value)
    if (idx === -1) {
      districts.value = [...districts.value, value]
    } else {
      districts.value = districts.value.filter((d) => d !== value)
    }
    applyFilters()
  }

  const clearDistricts = () => {
    districts.value = []
    applyFilters()
  }

  const goToPage = (nextPage) => {
    page.value = nextPage
    loadPlaces()
  }

  const fetchPlaceDetail = async (contentId) => {
    try {
      const { data } = await client.get(`/locations/${contentId}`)
      return data
    } catch (e) {
      return null
    }
  }

  const fetchNearby = async (contentId) => {
    try {
      const { data } = await client.get(`/locations/${contentId}/nearby`)
      return data
    } catch (e) {
      return { restaurants: [], lodgings: [] }
    }
  }

  return {
    activeCategory,
    districts,
    tag,
    sort,
    keyword,
    viewMode,
    places,
    page,
    total,
    pageSize: PAGE_SIZE,
    mapPoints,
    isMapLoading,
    mapLoadError,
    facets,
    isLoading,
    loadError,
    isFacetsLoading,
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
  }
}
