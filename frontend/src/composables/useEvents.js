import { ref, computed } from 'vue'
import { upcomingEvents as upcomingEventsData } from '../data/mockData'
import { useToast } from './useToast'

// 홈 화면 미리보기 위젯(UpcomingEvents) 전용 목업 데이터.
// 실제 축제/행사 데이터는 축제·행사 탭(useFestivals)에서 백엔드 API로 조회한다.
const pad2 = (n) => String(n).padStart(2, '0')

const year = ref(2026)
const month = ref(7)
const selectedDate = ref('2026-07-14')
const upcomingEvents = ref(upcomingEventsData)

export function useEvents() {
  const { showToast } = useToast()

  const daysInMonth = computed(() => new Date(year.value, month.value, 0).getDate())

  const dateStrFor = (day) => `${year.value}-${pad2(month.value)}-${pad2(day)}`

  const filteredEvents = computed(() =>
    upcomingEvents.value.filter((ev) => ev.dateSpan.includes(selectedDate.value))
  )

  const getWeekdayLabel = (day) => {
    const dateObj = new Date(year.value, month.value - 1, day)
    const weekDays = ['일', '월', '화', '수', '목', '금', '토']
    return weekDays[dateObj.getDay()]
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
  }

  const getEventsForDate = (dateStr) =>
    upcomingEvents.value.filter((ev) => ev.dateSpan.includes(dateStr))

  const openEventDetails = (ev) => {
    showToast(`[${ev.category}] ${ev.title} 상세 조회: 진행 기간은 ${ev.dateStr} 입니다.`)
  }

  return {
    year,
    month,
    daysInMonth,
    selectedDate,
    upcomingEvents,
    filteredEvents,
    getWeekdayLabel,
    dateStrFor,
    goToMonth,
    getEventsForDate,
    openEventDetails
  }
}
