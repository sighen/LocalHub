import { ref, computed } from 'vue'
import client from '../api/client'

// 홈 화면 미리보기 위젯(UpcomingEvents)도 축제·행사 탭과 같은 백엔드
// /festivals API를 사용한다. 같은 달의 데이터를 공유하도록 모듈 스코프에 둔다.
const pad2 = (n) => String(n).padStart(2, '0')
const toCompactDate = (isoDateStr) => isoDateStr.replace(/-/g, '')

const today = new Date()
const year = ref(today.getFullYear())
const month = ref(today.getMonth() + 1)
const selectedDate = ref(`${year.value}-${pad2(month.value)}-${pad2(today.getDate())}`)

const events = ref([])
const isLoading = ref(false)
const loadError = ref(false)

export function useEvents() {
  const daysInMonth = computed(() => new Date(year.value, month.value, 0).getDate())

  const dateStrFor = (day) => `${year.value}-${pad2(month.value)}-${pad2(day)}`

  const filteredEvents = computed(() => {
    const compact = toCompactDate(selectedDate.value)
    return events.value.filter(
      (ev) => ev.event_start_date && ev.event_end_date && ev.event_start_date <= compact && ev.event_end_date >= compact
    )
  })

  const getWeekdayLabel = (day) => {
    const dateObj = new Date(year.value, month.value - 1, day)
    const weekDays = ['일', '월', '화', '수', '목', '금', '토']
    return weekDays[dateObj.getDay()]
  }

  const loadEvents = async () => {
    isLoading.value = true
    loadError.value = false
    try {
      const { data } = await client.get('/festivals', {
        params: { date: `${year.value}-${pad2(month.value)}`, size: 100 }
      })
      events.value = data.items
    } catch (e) {
      loadError.value = true
      events.value = []
    } finally {
      isLoading.value = false
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
    selectedDate.value = dateStrFor(1)
    loadEvents()
  }

  return {
    year,
    month,
    daysInMonth,
    selectedDate,
    events,
    isLoading,
    loadError,
    filteredEvents,
    getWeekdayLabel,
    dateStrFor,
    goToMonth,
    loadEvents
  }
}
