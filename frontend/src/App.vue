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

const { fetchLiveWeather } = useWeather()
const { requestedTab, consumeRequestedTab } = useAppNavigation()

watch(requestedTab, (tab) => {
  if (tab) {
    currentTab.value = tab
    consumeRequestedTab()
  }
})

onMounted(() => {
  fetchLiveWeather()
})
</script>

<template>
  <div class="min-h-screen flex flex-col relative">
    <NavBar v-model:current-tab="currentTab" />

    <main class="flex-grow">
      <HomeView
        v-if="currentTab === 'home'"
        @go-community="currentTab = 'community'"
        @open-calendar="currentTab = 'festivals'"
        @open-location="currentTab = 'explore'"
      />
      <CommunityView v-else-if="currentTab === 'community'" />
      <ExploreView v-else-if="currentTab === 'explore'" />
      <FestivalsView v-else />
    </main>

    <ChatWidget />
    <ToastAlert />

    <FooterBar />
  </div>
</template>
