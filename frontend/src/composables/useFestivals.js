import { ref, computed } from 'vue'
import client from '../api/client'

const pad2 = (n) => String(n).padStart(2, '0')

const toCompactDate = (isoDateStr) => isoDateStr.replace(/-/g, '')

export const formatEventDate = (yyyymmdd) => {
  if (!yyyymmdd || yyyymmdd.length !== 8) return yyyymmdd
  return `${yyyymmdd.slice(0, 4)}.${yyyymmdd.slice(4, 6)}.${yyyymmdd.slice(6, 8)}`
}

export const formatEventPeriod = (start, end) => {
  if (!start && !end) return '기간 정보 없음'
  if (start === end) return formatEventDate(start)
  return `${formatEventDate(start)} ~ ${formatEventDate(end)}`
}

export function useFestivals() {
  const today = new Date()
  const year = ref(today.getFullYear())
  const month = ref(today.getMonth() + 1)
  const selectedDate = ref(`${year.value}-${pad2(month.value)}-${pad2(today.getDate())}`)

  const district = ref('')
  const viewMode = ref('calendar')

  const festivals = ref([])
  const facets = ref({ districts: [], tags: [] })

  const isLoading = ref(false)
  const loadError = ref(false)

  const monthLabel = computed(() => `${year.value}년 ${month.value}월`)

  const festivalsForDate = (dateStr) => {
    const compact = toCompactDate(dateStr)
    return festivals.value.filter(
      (f) => f.event_start_date && f.event_end_date && f.event_start_date <= compact && f.event_end_date >= compact
    )
  }

  const loadFestivals = async () => {
    isLoading.value = true
    loadError.value = false
    try {
      const { data } = await client.get('/festivals', {
        params: {
          date: `${year.value}-${pad2(month.value)}`,
          district: district.value || undefined,
          size: 100
        }
      })
      festivals.value = data.items
    } catch (e) {
      loadError.value = true
      festivals.value = []
    } finally {
      isLoading.value = false
    }
  }

  const loadFacets = async () => {
    try {
      const { data } = await client.get('/festivals/facets')
      facets.value = data
    } catch (e) {
      facets.value = { districts: [], tags: [] }
    }
  }

  const goToMonth = (delta) => {
    let nextMonth = month.value + delta
    let nextYear = year.value
    if (nextMonth < 1) {
      nextMonth = 12
      nextYear -= 1
    } else if (nextMonth > 12) {
      nextMonth = 1
      nextYear += 1
    }
    year.value = nextYear
    month.value = nextMonth
    selectedDate.value = `${nextYear}-${pad2(nextMonth)}-01`
    loadFestivals()
  }

  const selectDistrict = (value) => {
    district.value = value
    loadFestivals()
  }

  const fetchFestivalDetail = async (contentId) => {
    try {
      const { data } = await client.get(`/places/${contentId}`)
      return data
    } catch (e) {
      return null
    }
  }

  const fetchRelatedPosts = async (title) => {
    try {
      const { data } = await client.get('/posts', { params: { keyword: title, size: 5 } })
      return data.items
    } catch (e) {
      return []
    }
  }

  return {
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
    festivalsForDate,
    loadFestivals,
    loadFacets,
    goToMonth,
    selectDistrict,
    fetchFestivalDetail,
    fetchRelatedPosts
  }
}
