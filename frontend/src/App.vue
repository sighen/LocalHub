<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from './components/layout/NavBar.vue'
import FooterBar from './components/layout/FooterBar.vue'
import HomeView from './components/home/HomeView.vue'
import CommunityView from './components/community/CommunityView.vue'
import ExploreView from './components/explore/ExploreView.vue'
import FestivalsView from './components/festivals/FestivalsView.vue'
import WeatherDetailView from './components/weather/WeatherDetailView.vue'
import ToastAlert from './components/modals/ToastAlert.vue'
import ChatWidget from './components/chat/ChatWidget.vue'
import { useWeather } from './composables/useWeather'
import { useRouter } from './composables/useRouter'

const TABS = ['community', 'explore', 'festivals', 'weatherDetail']

const { segments, navigate, goBack } = useRouter()
const { fetchLiveWeather } = useWeather()

const currentTab = computed(() => (TABS.includes(segments.value[0]) ? segments.value[0] : 'home'))

const changeTab = (tab) => {
  navigate(tab === 'home' ? '/' : `/${tab}`)
}

const exploreCategory = ref('관광지')
const exploreTag = ref('')

const openExplore = (category) => {
  exploreCategory.value = category
  exploreTag.value = ''
  changeTab('explore')
}

const openExploreTag = (tag) => {
  exploreCategory.value = '관광지'
  exploreTag.value = tag
  changeTab('explore')
}

onMounted(() => {
  fetchLiveWeather()
})
</script>

<template>
  <div class="min-h-screen flex flex-col relative">
    <NavBar :current-tab="currentTab" @update:current-tab="changeTab" />

    <main class="flex-grow">
      <HomeView
        v-if="currentTab === 'home'"
        @go-community="changeTab('community')"
        @open-calendar="changeTab('festivals')"
        @open-explore="openExplore"
        @open-explore-tag="openExploreTag"
        @open-weather-detail="changeTab('weatherDetail')"
      />
      <CommunityView v-else-if="currentTab === 'community'" />
      <ExploreView v-else-if="currentTab === 'explore'" :initial-category="exploreCategory" :initial-tag="exploreTag" />
      <WeatherDetailView v-else-if="currentTab === 'weatherDetail'" @back="goBack" />
      <FestivalsView v-else />
    </main>

    <ChatWidget />
    <ToastAlert />

    <FooterBar />
  </div>
</template>
