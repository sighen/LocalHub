<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import L from 'leaflet'

const props = defineProps({
  places: { type: Array, required: true },
  height: { type: String, default: 'h-[520px]' }
})

const emit = defineEmits(['select-place'])

const mapContainer = ref(null)
let mapObj = null
let markers = []

const SEOUL_CENTER = [37.5665, 126.978]

const buildMarkerIcon = (highlighted) =>
  L.divIcon({
    className: 'custom-pin',
    html: `<div style="background-color: ${highlighted ? '#2563eb' : '#ef4444'}; border: 2px solid white; border-radius: 50%; width: 24px; height: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.15); display: flex; align-items: center; justify-content: center; color: white;"><i class="fa-solid fa-location-dot text-xs"></i></div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 24]
  })

const clearMarkers = () => {
  markers.forEach((m) => m.remove())
  markers = []
}

const renderMarkers = () => {
  if (!mapObj) return
  clearMarkers()

  const validPlaces = props.places.filter((p) => p.latitude && p.longitude)
  validPlaces.forEach((place) => {
    const marker = L.marker([place.latitude, place.longitude], { icon: buildMarkerIcon(validPlaces.length === 1) })
      .addTo(mapObj)
      .bindPopup(`<strong style="font-size:12px;">${place.title}</strong>`)

    marker.on('click', () => emit('select-place', place.content_id))
    markers.push(marker)
  })

  if (validPlaces.length === 1) {
    mapObj.setView([validPlaces[0].latitude, validPlaces[0].longitude], 15)
  } else if (validPlaces.length > 1) {
    const bounds = L.latLngBounds(validPlaces.map((p) => [p.latitude, p.longitude]))
    mapObj.fitBounds(bounds, { padding: [32, 32] })
  }
}

onMounted(() => {
  mapObj = L.map(mapContainer.value, { zoomControl: true }).setView(SEOUL_CENTER, 11)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(mapObj)
  renderMarkers()
})

onBeforeUnmount(() => {
  clearMarkers()
  if (mapObj) {
    mapObj.remove()
    mapObj = null
  }
})

watch(
  () => props.places,
  () => renderMarkers()
)
</script>

<template>
  <div ref="mapContainer" :class="['w-full rounded-2xl border border-slate-200 shadow-inner overflow-hidden relative z-10 bg-slate-100', height]"></div>
</template>
