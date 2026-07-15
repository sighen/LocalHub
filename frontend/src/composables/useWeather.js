import { ref } from 'vue'
import client from '../api/client'

const SEOUL_LAT = 37.5665
const SEOUL_LON = 126.978

function describeWeatherCode(code) {
  if (code === 0) return { icon: '☀️', label: '맑음' }
  if (code <= 3) return { icon: '⛅', label: '구름 조금' }
  if (code === 45 || code === 48) return { icon: '🌫️', label: '안개' }
  if (code >= 51 && code <= 57) return { icon: '🌦️', label: '이슬비' }
  if (code >= 61 && code <= 67) return { icon: '🌧️', label: '비' }
  if (code >= 71 && code <= 77) return { icon: '🌨️', label: '눈' }
  if (code >= 80 && code <= 82) return { icon: '🌦️', label: '소나기' }
  if (code >= 85 && code <= 86) return { icon: '🌨️', label: '눈 소나기' }
  if (code >= 95) return { icon: '⛈️', label: '뇌우' }
  return { icon: '☀️', label: '맑음' }
}

const weatherData = ref({
  temp: '28.7',
  icon: '☀️',
  status: '여행 적합 (맑음)'
})

const hourlyForecast = ref([])
const dailyForecast = ref([])
const isDetailLoading = ref(false)

export function useWeather() {
  const fetchLiveWeather = async () => {
    try {
      const { data } = await client.get('/weather/current')
      weatherData.value = { temp: data.temp, icon: data.icon, status: data.status }
    } catch (e) {
      console.warn('Live weather integration fallback used.')
    }
  }

  const fetchForecastDetail = async () => {
    isDetailLoading.value = true
    try {
      const response = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${SEOUL_LAT}&longitude=${SEOUL_LON}` +
          '&hourly=temperature_2m,weathercode,precipitation_probability' +
          '&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max' +
          '&timezone=Asia%2FSeoul&forecast_days=7'
      )
      if (!response.ok) return

      const data = await response.json()

      const nowHour = new Date().getHours()
      const todayStr = data.hourly.time[0].slice(0, 10)
      const startIndex = data.hourly.time.findIndex(
        (t) => t.startsWith(todayStr) && Number(t.slice(11, 13)) >= nowHour
      )
      const from = startIndex === -1 ? 0 : startIndex

      hourlyForecast.value = data.hourly.time.slice(from, from + 24).map((time, i) => {
        const idx = from + i
        const { icon } = describeWeatherCode(data.hourly.weathercode[idx])
        return {
          time,
          hourLabel: time.slice(11, 16),
          temp: Math.round(data.hourly.temperature_2m[idx]),
          pop: data.hourly.precipitation_probability[idx],
          icon
        }
      })

      dailyForecast.value = data.daily.time.slice(0, 7).map((date, idx) => {
        const { icon, label } = describeWeatherCode(data.daily.weathercode[idx])
        return {
          date,
          icon,
          label,
          tempMax: Math.round(data.daily.temperature_2m_max[idx]),
          tempMin: Math.round(data.daily.temperature_2m_min[idx]),
          pop: data.daily.precipitation_probability_max[idx]
        }
      })
    } catch (e) {
      console.warn('Weather detail fetch failed.')
    } finally {
      isDetailLoading.value = false
    }
  }

  return {
    weatherData,
    fetchLiveWeather,
    hourlyForecast,
    dailyForecast,
    isDetailLoading,
    fetchForecastDetail
  }
}
