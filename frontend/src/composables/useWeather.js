import { ref } from 'vue'
import { useToast } from './useToast'

export function useWeather() {
  const { showToast } = useToast()

  const weatherData = ref({
    temp: '28.7',
    icon: '☀️',
    status: '여행 적합 (맑음)'
  })

  const fetchLiveWeather = async () => {
    try {
      const response = await fetch(
        'https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current_weather=true'
      )
      if (!response.ok) return

      const data = await response.json()
      const temp = data.current_weather.temperature
      const code = data.current_weather.weathercode

      weatherData.value.temp = temp
      if (code >= 1 && code <= 3) {
        weatherData.value.icon = '⛅'
        weatherData.value.status = '야외 투어 적합 (구름 조금)'
      } else if (code >= 51 && code <= 67) {
        weatherData.value.icon = '🌦️'
        weatherData.value.status = '실내 박물관 투어 권장 (비 조금)'
      } else if (code >= 95) {
        weatherData.value.icon = '⛈️'
        weatherData.value.status = '경보 대비 요망 (천둥번개)'
      } else {
        weatherData.value.icon = '☀️'
        weatherData.value.status = '여행 최적 (맑음)'
      }
    } catch (e) {
      console.warn('Live weather integration fallback used.')
    }
  }

  const toggleWeatherDetail = () => {
    showToast(
      `[실시간 서울 기상] 온도: ${weatherData.value.temp}°C | 기상 컨디션: ${weatherData.value.status}. 서울 나들이 및 고궁 데이트를 즐겨보세요!`
    )
  }

  return { weatherData, fetchLiveWeather, toggleWeatherDetail }
}
