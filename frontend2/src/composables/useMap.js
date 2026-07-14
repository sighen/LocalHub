import { ref, nextTick } from 'vue'
import L from 'leaflet'
import { exploreSpots } from '../data/mockData'

export function useMap() {
  const isMapModalOpen = ref(false)
  let leafletMapObj = null

  const initLeafletMap = (targetSpot = null) => {
    if (leafletMapObj) {
      leafletMapObj.remove()
      leafletMapObj = null
    }

    const defaultCenter = [37.5665, 126.978]
    leafletMapObj = L.map('leaflet-modal-map', {
      zoomControl: true
    }).setView(targetSpot ? [targetSpot.lat, targetSpot.lng] : defaultCenter, targetSpot ? 14 : 11)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(leafletMapObj)

    exploreSpots.forEach((spot) => {
      const customMarker = L.divIcon({
        className: 'custom-pin',
        html: `<div style="background-color: #ef4444; border: 2px solid white; border-radius: 50%; width: 24px; height: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.15); display: flex; align-items: center; justify-content: center; color: white;"><i class="fa-solid fa-location-dot text-xs"></i></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 24]
      })

      const m = L.marker([spot.lat, spot.lng], { icon: customMarker })
        .addTo(leafletMapObj)
        .bindPopup(
          `<strong style="font-size:12px;">${spot.title}</strong><br><span style="font-size:10px; color:#666;">${spot.desc}</span>`
        )

      if (targetSpot && targetSpot.id === spot.id) {
        m.openPopup()
      }
    })
  }

  const openLeafletMapModal = () => {
    isMapModalOpen.value = true
    nextTick(() => initLeafletMap())
  }

  const openLocationMap = (spot) => {
    isMapModalOpen.value = true
    nextTick(() => initLeafletMap(spot))
  }

  return { isMapModalOpen, openLeafletMapModal, openLocationMap }
}
