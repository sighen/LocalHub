import { ref, computed } from 'vue'
import { upcomingEvents as upcomingEventsData } from '../data/mockData'
import { useToast } from './useToast'

// 홈 화면 미리보기 위젯(UpcomingEvents) 전용 목업 데이터.
// 실제 축제/행사 데이터는 축제·행사 탭(useFestivals)에서 백엔드 API로 조회한다.
const selectedDate = ref('2026-07-14')
const upcomingEvents = ref(upcomingEventsData)

export function useEvents() {
  const { showToast } = useToast()

  const filteredEvents = computed(() =>
    upcomingEvents.value.filter((ev) => ev.dateSpan.includes(selectedDate.value))
  )

  const getWeekdayLabel = (day) => {
    const dateObj = new Date(`2026-07-${day}`)
    const weekDays = ['일', '월', '화', '수', '목', '금', '토']
    return weekDays[dateObj.getDay()]
  }

  const getEventsForDate = (dateStr) =>
    upcomingEvents.value.filter((ev) => ev.dateSpan.includes(dateStr))

  const openEventDetails = (ev) => {
    showToast(`[${ev.category}] ${ev.title} 상세 조회: 진행 기간은 ${ev.dateStr} 입니다.`)
  }

  return {
    selectedDate,
    upcomingEvents,
    filteredEvents,
    getWeekdayLabel,
    getEventsForDate,
    openEventDetails
  }
}
