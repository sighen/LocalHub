<template>
  <div id="layout">
    <router-view />
    <!-- 모든 페이지에서 접근 가능한 챗봇 팝업 (C 담당) -->
    <ChatWidget />
  </div>
</template>

<script setup>
import ChatWidget from "./components/ChatWidget.vue";
</script>

<style>
* {
  box-sizing: border-box;
}
body {
  margin: 0;
  font-family: "Pretendard", -apple-system, sans-serif;
}
</style>
