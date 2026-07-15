<script setup>
import { ref, watch, onMounted } from 'vue'
import NavBar from './components/layout/NavBar.vue'
import FooterBar from './components/layout/FooterBar.vue'
import HomeView from './components/home/HomeView.vue'
import CommunityView from './components/community/CommunityView.vue'
import ExploreView from './components/explore/ExploreView.vue'
import FestivalsView from './components/festivals/FestivalsView.vue'
import ToastAlert from './components/modals/ToastAlert.vue'
import ChatWidget from './components/chat/ChatWidget.vue'
import { useWeather } from './composables/useWeather'
import { useAppNavigation } from './composables/useAppNavigation'

const currentTab = ref('home')
const exploreCategory = ref('관광지')
const exploreTag = ref('')

const { fetchLiveWeather } = useWeather()
const { requestedTab, consumeRequestedTab, pushBack } = useAppNavigation()

const changeTab = (tab) => {
  if (tab === currentTab.value) return
  const prevTab = currentTab.value
  pushBack(() => { currentTab.value = prevTab })
  currentTab.value = tab
}

watch(requestedTab, (tab) => {
  if (tab) {
    changeTab(tab)
    consumeRequestedTab()
  }
})

onMounted(() => {
  fetchLiveWeather()
})

const openExplore = (category) => {
  exploreCategory.value = category
  exploreTag.value = ''
  currentTab.value = 'explore'
}

const openExploreTag = (tag) => {
  exploreCategory.value = '관광지'
  exploreTag.value = tag
  currentTab.value = 'explore'
}
</script>

<template>
  <div class="min-h-screen flex flex-col relative">
    <NavBar :current-tab="currentTab" @update:current-tab="changeTab" />

    <main class="flex-grow">
      <HomeView
        v-if="currentTab === 'home'"
        @go-community="changeTab('community')"
        @open-calendar="changeTab('festivals')"
        @open-location="changeTab('explore')"
      />
      <CommunityView v-else-if="currentTab === 'community'" />
      <ExploreView v-else-if="currentTab === 'explore'" :initial-category="exploreCategory" :initial-tag="exploreTag" />
      <FestivalsView v-else />
    </main>

    <ChatWidget />
    <ToastAlert />

    <FooterBar />
  </div>
</template>
