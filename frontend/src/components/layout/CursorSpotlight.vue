<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// 마우스를 따라다니는 은은한 스포트라이트. 실제 마우스가 있는 기기에서만
// 켠다(터치 기기는 커서 개념이 없어 의미가 없고 리스너 비용만 생김).
const spotRef = ref(null)
const hasFinePointer = window.matchMedia?.('(hover: hover) and (pointer: fine)').matches

const onMove = (event) => {
  const el = spotRef.value
  if (!el) return
  el.style.setProperty('--x', `${event.clientX}px`)
  el.style.setProperty('--y', `${event.clientY}px`)
  el.style.opacity = '1'
}

const onLeave = () => {
  if (spotRef.value) spotRef.value.style.opacity = '0'
}

onMounted(() => {
  if (!hasFinePointer) return
  window.addEventListener('mousemove', onMove)
  document.addEventListener('mouseleave', onLeave)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onMove)
  document.removeEventListener('mouseleave', onLeave)
})
</script>

<template>
  <div v-if="hasFinePointer" ref="spotRef" class="cursor-spotlight"></div>
</template>

<style scoped>
.cursor-spotlight {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 30;
  opacity: 0;
  transition: opacity 0.3s ease;
  background: radial-gradient(600px circle at var(--x, 50%) var(--y, 50%), rgba(59, 130, 246, 0.08), transparent 60%);
}
</style>
