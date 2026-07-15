<script setup>
import { ref, computed, watch, nextTick, onMounted, onBeforeUpdate, onBeforeUnmount } from 'vue'
import { useEvents } from '../../composables/useEvents'
import { useFestivals, formatEventPeriod } from '../../composables/useFestivals'
import { secureImageUrl } from '../../utils/imageUrl'
import { resolvePlaceImage } from '../../utils/placeImage'
import FestivalDetailModal from '../festivals/FestivalDetailModal.vue'

const emit = defineEmits(['open-calendar'])

const {
  year,
  month,
  daysInMonth,
  selectedDate,
  isLoading,
  loadError,
  filteredEvents,
  getWeekdayLabel,
  dateStrFor,
  goToMonth,
  loadEvents
} = useEvents()

// 메인 화면에서는 탭 이동 없이 그 자리에서 팝업으로만 상세를 보여준다.
// (라우터로 /festivals/:id 이동하면 축제·행사 탭으로 전환되어 버리므로
// 별도로 이 컴포넌트 안에서만 상세 상태를 들고 있는다.)
const { fetchFestivalDetail } = useFestivals()
const selectedContentId = ref(null)
const detailPlace = ref(null)
const isDetailLoading = ref(false)
const detailLoadError = ref(false)

const openEventDetails = async (ev) => {
  selectedContentId.value = ev.content_id
  isDetailLoading.value = true
  detailLoadError.value = false
  try {
    const place = await fetchFestivalDetail(ev.content_id)
    if (!place) {
      detailLoadError.value = true
      return
    }
    detailPlace.value = place
  } finally {
    isDetailLoading.value = false
  }
}

const retryEventDetail = () => {
  if (selectedContentId.value) openEventDetails({ content_id: selectedContentId.value })
}

const closeEventDetail = () => {
  selectedContentId.value = null
  detailPlace.value = null
}

// 카드가 끝없이 둥글게 도는 느낌을 내기 위해 목록을 여러 벌 이어붙이고,
// translateX 위치를 한 벌 너비만큼씩 순환시킨다(끝에 닿으면 다음 벌이
// 똑같은 카드라 이어 붙인 것처럼 안 보이게 자연스럽게 이어진다).
const LOOP_COPIES = 8
const loopedEvents = computed(() => {
  if (filteredEvents.value.length === 0) return []
  const copies = []
  for (let i = 0; i < LOOP_COPIES; i += 1) copies.push(...filteredEvents.value)
  return copies
})

const trackRef = ref(null)
const innerTrackRef = ref(null)
let position = 0
let velocity = 0
let isHovering = false
let rafId = null
const MAX_SPEED = 9

const cardRefs = ref([])
const cardFocus = ref([])

onBeforeUpdate(() => {
  cardRefs.value = []
})

const updateFocus = () => {
  const el = trackRef.value
  if (!el || cardRefs.value.length === 0) return
  const containerCenter = el.getBoundingClientRect().left + el.clientWidth / 2
  const falloff = el.clientWidth / 2 + 24

  cardFocus.value = cardRefs.value.map((card) => {
    if (!card) return 0
    const rect = card.getBoundingClientRect()
    const cardCenter = rect.left + rect.width / 2
    const dist = Math.abs(cardCenter - containerCenter)
    return Math.max(0, 1 - dist / falloff)
  })
}

const cardStyle = (index) => {
  const focus = cardFocus.value[index] ?? 0
  const scale = 0.9 + focus * 0.14
  const opacity = 0.8 + focus * 0.2
  return {
    transform: `scale(${scale})`,
    opacity,
    zIndex: Math.round(focus * 10)
  }
}

const animateTrack = () => {
  const inner = innerTrackRef.value
  if (!inner || filteredEvents.value.length === 0) {
    rafId = null
    return
  }

  if (!isHovering) {
    velocity *= 0.9
    if (Math.abs(velocity) < 0.05) velocity = 0
  }

  const setWidth = inner.scrollWidth / LOOP_COPIES
  if (setWidth > 0) {
    position += velocity
    // 한 벌 너비를 벗어나면 그만큼 되돌려서, 항상 앞뒤로 카드가 이어져
    // 보이는 가운데 구간 안에서만 움직이게 한다 (무한 루프 트릭).
    position = ((position % setWidth) + setWidth) % setWidth
  }

  const anchor = Math.floor(LOOP_COPIES / 2) * setWidth
  inner.style.transform = `translateX(${-(anchor + position)}px)`
  updateFocus()

  if (isHovering || Math.abs(velocity) > 0.01) {
    rafId = requestAnimationFrame(animateTrack)
  } else {
    rafId = null
  }
}

const getClientX = (event) => (event.touches ? event.touches[0].clientX : event.clientX)

const onTrackPointerMove = (event) => {
  const el = trackRef.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  const ratio = ((getClientX(event) - rect.left) / rect.width) * 2 - 1
  velocity = Math.min(1, Math.max(-1, ratio)) * MAX_SPEED
  isHovering = true
  if (!rafId) rafId = requestAnimationFrame(animateTrack)
}

const onTrackPointerLeave = () => {
  isHovering = false
}

watch(filteredEvents, () => {
  position = 0
  velocity = 0
  nextTick(updateFocus)
})

onMounted(() => {
  loadEvents()
})

onBeforeUnmount(() => {
  if (rafId) cancelAnimationFrame(rafId)
})
</script>

<template>
  <section id="upcoming-section" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
    <div class="text-center space-y-2">
      <span class="text-xs font-extrabold text-blue-600 uppercase tracking-widest">서울에서 진행되는 다양한 이벤트</span>
      <h2 class="text-3xl font-black text-slate-900 tracking-tight">서울 Upcoming!</h2>
    </div>

    <div class="bg-white border border-slate-100 rounded-2xl p-4 shadow-sm flex items-center gap-3">
      <div class="bg-slate-100 px-4 py-2 rounded-xl text-center shrink-0">
        <span class="text-[10px] text-slate-400 font-bold block uppercase">{{ year }}</span>
        <div class="flex items-center justify-center gap-3">
          <button @click="goToMonth(-1)" class="text-slate-400 hover:text-slate-700 font-black text-sm transition px-0.5">&lt;</button>
          <span class="text-lg font-black text-slate-800">{{ String(month).padStart(2, '0') }}월</span>
          <button @click="goToMonth(1)" class="text-slate-400 hover:text-slate-700 font-black text-sm transition px-0.5">&gt;</button>
        </div>
      </div>

      <div class="flex-grow overflow-x-auto flex gap-2 py-1 custom-scrollbar scroll-smooth">
        <button
          v-for="day in daysInMonth"
          :key="day"
          @click="selectedDate = dateStrFor(day)"
          :class="['px-4 py-2.5 rounded-xl text-center min-w-[56px] transition duration-150 shrink-0 border', selectedDate === dateStrFor(day) ? 'bg-blue-600 border-blue-600 text-white font-bold shadow-md shadow-blue-500/10' : 'bg-slate-50 border-slate-100 text-slate-600 hover:bg-slate-100']"
        >
          <span class="text-xs block opacity-80">{{ getWeekdayLabel(day) }}</span>
          <span class="text-base font-extrabold">{{ day }}</span>
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="p-16 text-center text-slate-400 space-y-2 bg-white border border-slate-100 rounded-2xl">
      <i class="fa-solid fa-spinner fa-spin text-3xl block mb-2"></i>
      <p class="text-sm font-semibold">불러오는 중입니다...</p>
    </div>
    <div v-else-if="loadError" class="p-16 text-center text-slate-400 space-y-3 bg-white border border-slate-100 rounded-2xl">
      <i class="fa-solid fa-triangle-exclamation text-4xl block mb-2 text-amber-400"></i>
      <p class="text-sm font-semibold text-slate-500">이벤트를 불러오지 못했어요. 잠시 후 다시 시도해주세요.</p>
      <button @click="loadEvents" class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-700 transition">다시 시도</button>
    </div>
    <div v-else-if="filteredEvents.length === 0" class="p-16 text-center text-slate-400 space-y-2 bg-white border border-slate-100 rounded-2xl">
      <i class="fa-regular fa-calendar-xmark text-3xl block mb-2"></i>
      <p class="text-sm font-semibold">선택한 날짜에 예정된 이벤트가 없습니다.</p>
    </div>
    <div
      v-else
      ref="trackRef"
      class="overflow-hidden py-4 cursor-ew-resize"
      @mousemove="onTrackPointerMove"
      @mouseleave="onTrackPointerLeave"
      @touchmove="onTrackPointerMove"
      @touchend="onTrackPointerLeave"
      @touchcancel="onTrackPointerLeave"
    >
      <div ref="innerTrackRef" class="flex items-center gap-5 w-max">
        <div
          v-for="(ev, index) in loopedEvents"
          :key="index"
          ref="cardRefs"
          :style="cardStyle(index)"
          class="w-44 sm:w-52 shrink-0 transition-[transform,opacity] duration-200 ease-out"
        >
          <div class="flip-card aspect-[3/4] cursor-pointer" @click="openEventDetails(ev)">
            <div class="flip-card-inner">
              <div class="flip-card-front rounded-2xl border border-slate-100 shadow-sm overflow-hidden bg-slate-100">
                <template v-if="resolvePlaceImage(ev)">
                  <img
                    :src="secureImageUrl(resolvePlaceImage(ev))"
                    :alt="ev.title"
                    class="w-full h-full object-cover"
                  />
                </template>
                <template v-else>
                  <div class="w-full h-full bg-slate-200"></div>
                </template>
                <span class="absolute top-3 left-3 px-2.5 py-1 bg-blue-600 text-white text-[10px] font-black rounded-lg shadow-sm">진행/예정</span>
                <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent p-4 space-y-1">
                  <span v-if="ev.district_name" class="text-[10px] font-bold text-white bg-white/20 px-2 py-0.5 rounded backdrop-blur-sm">{{ ev.district_name }}</span>
                  <h3 class="text-sm font-black text-white truncate">{{ ev.title }}</h3>
                </div>
              </div>

              <div class="flip-card-back rounded-2xl border border-slate-100 shadow-sm bg-white p-4 flex flex-col">
                <span v-if="ev.district_name" class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded w-fit">{{ ev.district_name }}</span>
                <h3 class="text-sm font-black text-slate-800 mt-2 leading-snug line-clamp-2">{{ ev.title }}</h3>
                <p class="text-[11px] text-slate-400 font-semibold mt-1.5">
                  <i class="fa-regular fa-calendar mr-1"></i>{{ formatEventPeriod(ev.event_start_date, ev.event_end_date) }}
                </p>
                <p v-if="ev.addr1" class="text-[11px] text-slate-400 mt-1 truncate">
                  <i class="fa-solid fa-location-dot mr-1"></i>{{ ev.addr1 }}
                </p>
                <p v-if="ev.overview" class="text-[11px] text-slate-500 leading-relaxed line-clamp-4 mt-3">{{ ev.overview }}</p>
                <span class="mt-auto pt-2 text-[10px] font-bold text-blue-600">자세히 보기 <i class="fa-solid fa-arrow-right ml-0.5"></i></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center pt-2">
      <button @click="emit('open-calendar')" class="px-6 py-3 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-full text-xs font-black transition shadow-sm border border-blue-100/30">
        달력으로 전체 일정 보기 <i class="fa-solid fa-chevron-right ml-1"></i>
      </button>
    </div>

    <FestivalDetailModal
      v-if="selectedContentId"
      :place="detailPlace"
      :is-loading="isDetailLoading"
      :load-error="detailLoadError"
      @close="closeEventDetail"
      @retry="retryEventDetail"
    />
  </section>
</template>

<style scoped>
.flip-card {
  perspective: 1200px;
  position: relative;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}
.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}
.flip-card-front,
.flip-card-back {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}
.flip-card-back {
  transform: rotateY(180deg);
}
</style>
