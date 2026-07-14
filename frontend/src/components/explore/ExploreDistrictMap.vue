<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import L from 'leaflet'
import seoulDistricts from '../../data/seoulDistricts.geo.json'

const props = defineProps({
  districts: { type: Array, required: true }
})

const emit = defineEmits(['toggle-district', 'clear-districts'])

const mapContainer = ref(null)
let mapObj = null
let geoLayer = null

const BASE_STYLE = { color: '#cbd5e1', weight: 1, fillColor: '#e2e8f0', fillOpacity: 0.6 }
const SELECTED_STYLE = { color: '#2563eb', weight: 1.5, fillColor: '#3b82f6', fillOpacity: 0.75 }
const HOVER_STYLE = { color: '#2563eb', weight: 1.5, fillColor: '#93c5fd', fillOpacity: 0.75 }

const styleFor = (name) => (props.districts.includes(name) ? SELECTED_STYLE : BASE_STYLE)

const refreshStyles = () => {
  if (!geoLayer) return
  geoLayer.eachLayer((layer) => layer.setStyle(styleFor(layer.feature.properties.name)))
}

onMounted(() => {
  mapObj = L.map(mapContainer.value, {
    zoomControl: false,
    dragging: true,
    scrollWheelZoom: true,
    doubleClickZoom: false,
    boxZoom: false,
    attributionControl: false
  })

  geoLayer = L.geoJSON(seoulDistricts, {
    style: (feature) => styleFor(feature.properties.name),
    onEachFeature: (feature, layer) => {
      const name = feature.properties.name
      layer.bindTooltip(name, { permanent: true, direction: 'center', className: 'district-label' })
      layer.on('mouseover', () => layer.setStyle(HOVER_STYLE))
      layer.on('mouseout', () => layer.setStyle(styleFor(name)))
      layer.on('click', () => emit('toggle-district', name))
    }
  }).addTo(mapObj)

  mapObj.fitBounds(geoLayer.getBounds(), { padding: [2, 2] })
  const baseZoom = mapObj.getZoom()
  mapObj.setMinZoom(baseZoom)
  mapObj.setMaxZoom(baseZoom + 3)
})

onBeforeUnmount(() => {
  if (mapObj) {
    mapObj.remove()
    mapObj = null
  }
})

watch(() => props.districts, refreshStyles, { deep: true })
</script>

<template>
  <div class="space-y-2">
    <h4 class="text-xs font-black text-slate-700">권역 <span class="font-normal text-slate-400">(복수 선택 가능)</span></h4>
    <div class="relative">
      <button
        v-if="districts.length"
        @click="emit('clear-districts')"
        class="absolute top-3 right-3 z-[500] px-3 py-1.5 bg-white/90 backdrop-blur border border-slate-200 rounded-lg text-[11px] font-bold text-slate-600 hover:bg-white shadow-sm transition"
      >
        선택 해제
      </button>
      <div ref="mapContainer" class="w-full h-[420px] rounded-2xl border border-slate-200 bg-white overflow-hidden cursor-pointer"></div>
    </div>
  </div>
</template>

<style scoped>
:deep(.district-label) {
  background: transparent;
  border: none;
  box-shadow: none;
  font-size: 10px;
  font-weight: 800;
  color: #475569;
  padding: 0;
}
</style>
