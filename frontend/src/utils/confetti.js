// 라이브러리 없이 클릭 지점에서 작은 색종이 조각을 흩뿌리는 마이크로 인터랙션.
// 파티클을 body에 직접 붙였다가 애니메이션이 끝나면 제거한다.
const COLORS = ['#3b82f6', '#f59e0b', '#ef4444', '#10b981', '#8b5cf6', '#ec4899']

export function burstConfetti(x, y, count = 14) {
  for (let i = 0; i < count; i += 1) {
    const el = document.createElement('span')
    const angle = Math.random() * Math.PI * 2
    const distance = 40 + Math.random() * 50
    const dx = Math.cos(angle) * distance
    const dy = Math.sin(angle) * distance
    const size = 5 + Math.random() * 5
    const color = COLORS[Math.floor(Math.random() * COLORS.length)]
    const rounded = Math.random() > 0.5

    el.style.cssText = `
      position: fixed;
      left: ${x}px;
      top: ${y}px;
      width: ${size}px;
      height: ${size}px;
      background: ${color};
      border-radius: ${rounded ? '50%' : '2px'};
      pointer-events: none;
      z-index: 99999;
      opacity: 1;
      transform: translate(-50%, -50%) rotate(0deg);
      transition: transform 0.6s cubic-bezier(0.17, 0.67, 0.5, 1), opacity 0.6s ease-out;
    `
    document.body.appendChild(el)

    requestAnimationFrame(() => {
      el.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) rotate(${Math.random() * 360}deg)`
      el.style.opacity = '0'
    })

    setTimeout(() => el.remove(), 650)
  }
}
