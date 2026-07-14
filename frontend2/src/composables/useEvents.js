import { ref, computed } from 'vue'
import { upcomingEvents as upcomingEventsData } from '../data/mockData'
import { useToast } from './useToast'

// UpcomingEvents 섹션과 CalendarModal이 같은 selectedDate 상태를 공유해야 하므로
// 모듈 스코프에서 한 번만 생성합니다 (싱글턴 패턴).
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
