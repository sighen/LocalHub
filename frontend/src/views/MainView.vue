<template>
  <main class="main-page">
    <!-- B: 히어로 배너, 인터랙션, 애니메이션은 여기서 자유롭게 확장 -->
    <section class="hero">
      <h1>지역 관광 커뮤니티</h1>
      <p>서울 곳곳의 관광지·축제 정보와 커뮤니티를 한 곳에서</p>
    </section>

    <section class="highlights">
      <h2>추천 스팟</h2>
      <!-- TODO(B): /api/locations 로 인기 스팟 카드 렌더링 -->
    </section>

    <section class="upcoming-festivals">
      <h2>다가오는 축제</h2>
      <!-- TODO(B): /api/festivals 로 카드 렌더링 -->
    </section>
  </main>
</template>

<script setup>
// B: 필요한 애니메이션 라이브러리(예: gsap, @vueuse/motion 등)는 자유롭게 추가
</script>

<style scoped>
.hero {
  padding: 80px 24px;
  text-align: center;
}
</style>
