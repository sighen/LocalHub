<script setup>
import { ref, onMounted } from 'vue'
import NavBar from './components/layout/NavBar.vue'
import FooterBar from './components/layout/FooterBar.vue'
import HomeView from './components/home/HomeView.vue'
import CommunityView from './components/community/CommunityView.vue'
import CalendarModal from './components/modals/CalendarModal.vue'
import MapModal from './components/modals/MapModal.vue'
import ToastAlert from './components/modals/ToastAlert.vue'
import ChatWidget from './components/chat/ChatWidget.vue'
import { useWeather } from './composables/useWeather'
import { useMap } from './composables/useMap'

const currentTab = ref('home')
const isCalendarModalOpen = ref(false)

const { fetchLiveWeather } = useWeather()
const { isMapModalOpen, openLeafletMapModal, openLocationMap } = useMap()

const openFullCalendarModal = () => {
  isCalendarModalOpen.value = true
}

onMounted(() => {
  fetchLiveWeather()
})
</script>

<template>
  <div class="min-h-screen flex flex-col relative">
    <NavBar
      v-model:current-tab="currentTab"
      @open-calendar="openFullCalendarModal"
      @open-map="openLeafletMapModal"
    />

    <main class="flex-grow">
      <HomeView
        v-if="currentTab === 'home'"
        @go-community="currentTab = 'community'"
        @open-calendar="openFullCalendarModal"
        @open-location="openLocationMap"
      />
      <CommunityView v-else />
    </main>

    <ChatWidget />
    <ToastAlert />

    <CalendarModal v-if="isCalendarModalOpen" @close="isCalendarModalOpen = false" />
    <MapModal v-if="isMapModalOpen" @close="isMapModalOpen = false" />

    <FooterBar />
  </div>
</template>
