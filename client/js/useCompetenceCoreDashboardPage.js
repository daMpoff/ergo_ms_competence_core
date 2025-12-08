import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  LayoutDashboard,
  CircuitBoard,
  BadgeCheck,
  BriefcaseBusiness,
  TrendingUp,
  Layers,
  RefreshCcw,
  Star,
  Flame,
  Rocket,
  ArrowUpRight,
  ArrowDownRight,
  Crown,
} from 'lucide-vue-next'

export function useCompetenceCoreDashboardPage() {
  const router = useRouter()

  const periods = [
    { label: '6 мес', value: 6 },
    { label: '12 мес', value: 12 },
    { label: '24 мес', value: 24 },
  ]
  const selectedPeriod = ref(12)

  const techPool = ['Python', 'JavaScript', 'Java', 'Go', 'SQL', 'TypeScript', 'C#', 'Kotlin']
  const categoryPool = ['Backend', 'Data', 'Frontend', 'Cloud', 'DevOps']
  const selectedTechnologies = ref(['Python', 'JavaScript', 'Java', 'Go', 'SQL'])
  const selectedCategories = ref([...categoryPool])

  const kpis = computed(() => ([
    { id: 'tech', label: 'Технологий', value: 602, accent: 'text-danger', icon: Layers },
    { id: 'competences', label: 'Компетенций', value: 186, accent: 'text-muted', icon: BadgeCheck },
    { id: 'vacancies', label: 'Профилей вакансий', value: 2304, accent: 'text-muted', icon: BriefcaseBusiness },
    { id: 'updates', label: 'Обновлений за неделю', value: 342, accent: 'text-muted', icon: RefreshCcw },
  ]))

  const months = computed(() => {
    const total = selectedPeriod.value
    const labels = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
    if (total === 24) return [...labels, ...labels]
    if (total === 6) return labels.slice(6)
    return labels
  })

  const seededNoise = (key, i, amp = 3.4) => {
    let seed = 0
    for (let j = 0; j < key.length; j++) seed += key.charCodeAt(j) * (j + 3)
    const raw = Math.sin(i * 0.8 + seed) * amp + Math.cos(i / 3 + seed) * (amp * 0.35)
    return raw
  }

  const pulse = (i, center, strength) => {
    const dist = Math.abs(i - center)
    return Math.max(0, strength - dist * 0.9)
  }

  const generateSeries = (names, baseMap) => {
    const total = selectedPeriod.value
    const arr = []
    names.forEach((name, idx) => {
      const base = baseMap[name] ?? 60 + idx * 4
      const growth = 0.22 + idx * 0.07
      const data = []
      const mid = Math.floor(total * 0.45)
      const late = Math.floor(total * 0.75)
      for (let i = 0; i < total; i++) {
        const seasonal = Math.sin(i / 2.6) * 3.5 + Math.cos(i / 4.2) * 1.8
        const trend = base + i * growth
        const accel = i > mid ? (i - mid) * 0.08 : 0
        const spike = pulse(i, mid, 4.5) + pulse(i, late, -3.2)
        const noise = seededNoise(name, i, 2.6)
        data.push(Math.max(30, Math.round(trend + seasonal + accel + spike + noise)))
      }
      arr.push({ name, data })
    })
    return arr
  }

  const setPeriod = (value) => {
    selectedPeriod.value = value
  }

  const toggleTechnology = (name) => {
    const exists = selectedTechnologies.value.includes(name)
    if (exists && selectedTechnologies.value.length <= 2) return
    selectedTechnologies.value = exists
      ? selectedTechnologies.value.filter((t) => t !== name)
      : [...selectedTechnologies.value, name]
  }

  const toggleCategory = (name) => {
    const exists = selectedCategories.value.includes(name)
    if (exists && selectedCategories.value.length <= 2) return
    selectedCategories.value = exists
      ? selectedCategories.value.filter((c) => c !== name)
      : [...selectedCategories.value, name]
  }

  const popularityTrendSeries = computed(() => {
    const baseMap = {
      Python: 76,
      JavaScript: 70,
      Java: 65,
      Go: 50,
      SQL: 68,
      TypeScript: 64,
      'C#': 62,
      Kotlin: 59,
    }
    return generateSeries(selectedTechnologies.value, baseMap)
  })

  const popularityTrendOptions = computed(() => ({
    chart: {
      id: 'popularity-trend',
      toolbar: { show: false },
      animations: { enabled: true, easing: 'easeinout', speed: 450 }
    },
    colors: ['#dc3545', '#6c757d', '#495057', '#adb5bd', '#ced4da', '#868e96', '#e03131'],
    stroke: { curve: 'smooth', width: 2.6 },
    markers: { size: 0, hover: { size: 4 } },
    dataLabels: { enabled: false },
    grid: { borderColor: '#e9ecef', strokeDashArray: 3 },
    xaxis: {
      categories: months.value,
      axisBorder: { show: false },
      axisTicks: { show: false },
      labels: { style: { colors: '#6c757d' } },
    },
    yaxis: { labels: { formatter: (val) => Math.round(val), style: { colors: '#6c757d' } } },
    tooltip: { shared: true, theme: 'light' },
    legend: { position: 'top', horizontalAlign: 'left', fontSize: '12px' },
    title: {
      text: `Динамика популярности технологий (${selectedPeriod.value} мес)`,
      style: { fontSize: '13px', fontWeight: 600, color: '#343a40' },
    },
  }))

  const categoryStackedSeries = computed(() => {
    const total = selectedPeriod.value
    const cfg = {
      Backend:   { base: 32, growth: 0.26, amp: 2.4, phase: 0.6, midBump: 1.4 },
      Data:      { base: 24, growth: 0.19, amp: 2.1, phase: 1.2, midBump: 1.6 },
      Frontend:  { base: 19, growth: 0.17, amp: 1.8, phase: 0.9, midBump: 1.2 },
      Cloud:     { base: 14, growth: 0.21, amp: 2.0, phase: 1.6, midBump: 1.9 },
      DevOps:    { base: 11, growth: 0.16, amp: 1.7, phase: 0.4, midBump: 1.1 },
    }
    return selectedCategories.value.map((category) => {
      const { base = 15, growth = 0.18, amp = 1.6, phase = 0, midBump = 1.2 } = cfg[category] || {}
      const data = []
      for (let i = 0; i < total; i++) {
        const seasonal = Math.sin(i / 2.9 + phase) * amp + Math.cos(i / 5.2 + phase) * (amp * 0.55)
        const trend = base + i * growth
        const midCycle = (i % 12 >= 3 && i % 12 <= 6) ? midBump : 0
        const noise = seededNoise(category, i, 1.4)
        data.push(Math.max(6, Math.round(trend + seasonal + midCycle + noise * 0.4)))
      }
      return { name: category, data }
    })
  })

  const categoryStackedOptions = computed(() => ({
    chart: { type: 'area', stacked: true, toolbar: { show: false } },
    colors: ['#dc3545', '#6c757d', '#495057', '#adb5bd', '#ced4da', '#868e96'],
    dataLabels: { enabled: false },
    stroke: { curve: 'smooth', width: 2.35 },
    xaxis: { categories: months.value },
    tooltip: { shared: true, theme: 'light' },
    legend: { position: 'top', horizontalAlign: 'left', fontSize: '12px' },
    fill: { opacity: 0.65, type: 'gradient', gradient: { shadeIntensity: 0.25, opacityFrom: 0.9, opacityTo: 0.6 } },
    title: {
      text: `Категории технологий — динамика (${selectedPeriod.value} мес)`,
      style: { fontSize: '13px', fontWeight: 600, color: '#343a40' },
    },
  }))

  const topTechnologies = computed(() => ([
    { name: 'Python', popularity: 94, delta30: 3.4 },
    { name: 'JavaScript', popularity: 88, delta30: 1.6 },
    { name: 'Java', popularity: 85, delta30: 1.1 },
    { name: 'SQL', popularity: 82, delta30: 1.9 },
    { name: 'TypeScript', popularity: 78, delta30: 2.4 },
    { name: 'C#', popularity: 74, delta30: -0.3 },
    { name: 'Go', popularity: 70, delta30: 2.8 },
  ]))

  const topTechnologiesSeries = computed(() => ([
    { name: 'Популярность', data: topTechnologies.value.map((t) => t.popularity) }
  ]))

  const topTechnologiesOptions = computed(() => ({
    chart: { type: 'bar', toolbar: { show: false } },
    colors: ['#dc3545'],
    plotOptions: {
      bar: {
        borderRadius: 6,
        horizontal: true,
      }
    },
    dataLabels: {
      enabled: true,
      style: { colors: ['#f8f9fa'], fontSize: '12px', fontWeight: 700 },
      offsetX: 8,
      formatter: (val, opts) => {
        const idx = opts.dataPointIndex
        const delta = topTechnologies.value[idx]?.delta30 ?? 0
        const sign = delta > 0 ? '+' : ''
        return `${val}% (${sign}${delta.toFixed(1)} п.п.)`
      }
    },
    xaxis: {
      categories: topTechnologies.value.map((t) => t.name),
      labels: { formatter: (val) => Math.round(val) }
    },
    tooltip: { y: { formatter: (val) => `${val} %` } },
    title: {
      text: 'Топ технологий (текущая популярность)',
      style: { fontSize: '13px', fontWeight: 600, color: '#343a40' },
    }
  }))

  const levelSeries = computed(() => ([42, 37, 16, 5]))

  const levelOptions = computed(() => ({
    chart: { type: 'donut' },
    labels: ['Middle', 'Senior', 'Junior', 'Expert'],
    colors: ['#dc3545', '#6c757d', '#adb5bd', '#ced4da'],
    legend: { position: 'bottom', fontSize: '12px' },
    dataLabels: { enabled: false },
    plotOptions: {
      pie: {
        expandOnClick: false,
        donut: {
          size: '68%',
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: '12px',
              color: '#6c757d',
              offsetY: 4,
            },
            value: {
              show: true,
              fontSize: '20px',
              fontWeight: 700,
              color: '#343a40',
              formatter: (val) => `${Math.round(val)}%`,
            },
            total: {
              show: true,
              label: 'Всего',
              fontSize: '11px',
              color: '#6c757d',
              formatter: () => '100%',
            }
          }
        }
      }
    }
  }))

  const growthSignals = computed(() => ([
    {
      name: 'Python',
      delta: 3.4,
      comment: 'Усиление ML+backend продуктов; спрос на API, очереди, аналитика',
      icon: ArrowUpRight,
      trend: [0.8, 1.2, 1.5, 1.9, 2.3, 2.8, 3.4],
    },
    {
      name: 'Go',
      delta: 2.8,
      comment: 'Микросервисы и облако; рост вакансий в highload и инфраструктуре',
      icon: ArrowUpRight,
      trend: [0.5, 0.9, 1.2, 1.6, 2.0, 2.4, 2.8],
    },
    {
      name: 'TypeScript',
      delta: 2.4,
      comment: 'Укрепление typed-стека в фронтенде; рост SPA/SPA+SSR',
      icon: ArrowUpRight,
      trend: [0.7, 1.0, 1.2, 1.5, 1.7, 2.0, 2.4],
    },
    {
      name: 'C#',
      delta: -0.3,
      comment: 'Стабилизация набора; фокус на поддержке существующих систем',
      icon: ArrowDownRight,
      trend: [0.3, 0.2, 0.1, 0.0, -0.1, -0.2, -0.3],
    },
    {
      name: 'Java',
      delta: 1.1,
      comment: 'Enterprise и финтех держат стабильный спрос; прирост умеренный',
      icon: ArrowUpRight,
      trend: [0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.1],
    },
  ].map((row) => ({
    ...row,
    trendMin: Math.min(...row.trend),
    trendMax: Math.max(...row.trend),
  }))))

  const highlights = computed(() => ({
    fastest: { name: 'Go', delta: '+21% за 12 мес', note: 'Скачок за счёт микросервисов и облачных миграций.', icon: Rocket },
    vacancy: { name: 'Backend Developer (Python)', window: 'Последние 30 дней', note: 'API, очереди, Postgres, Celery — высокий спрос.', icon: Flame },
    category: { name: 'Backend направление', share: '42% доли', note: 'Лидирует за счёт Python/Go и микросервисной архитектуры.', icon: Crown },
  }))

  const comparisonSeries = computed(() => {
    const items = topTechnologies.value.slice(0, 5)
    const current = items.map((t) => t.popularity)
    const previous = items.map((t) => Math.max(0, +(t.popularity - t.delta30).toFixed(1)))
    return [
      { name: 'Прошлый период', data: previous },
      { name: 'Текущий период', data: current },
    ]
  })

  const comparisonOptions = computed(() => ({
    chart: { type: 'bar', stacked: false, toolbar: { show: false }, parentHeightOffset: 0 },
    plotOptions: {
      bar: {
        horizontal: true,
        barHeight: '70%',
        borderRadius: 8,
        columnWidth: '60%',
        dataLabels: {
          position: 'top',
        },
      }
    },
    colors: ['#6c757d', '#dc3545'],
    dataLabels: {
      enabled: false,
    },
    legend: {
      position: 'top',
      horizontalAlign: 'left',
      fontSize: '12px',
      markers: { fillColors: ['#6c757d', '#dc3545'], radius: 7 },
      labels: { colors: '#6c757d' },
      itemMargin: { horizontal: 10 },
    },
    xaxis: {
      categories: topTechnologies.value.slice(0, 5).map((t) => t.name),
      axisBorder: { show: false },
      axisTicks: { show: false },
      labels: {
        formatter: (val) => `${Math.round(val)}%`,
        style: { colors: '#6c757d' },
      },
    },
    grid: { borderColor: '#e9ecef', strokeDashArray: 4, padding: { top: 0, bottom: 0 } },
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: (val) => `${val}%`,
      }
    },
    title: {
      text: 'Сравнение с прошлым периодом (топ-5)',
      style: { fontSize: '13px', fontWeight: 600, color: '#343a40' },
    },
  }))

  const forecastSeries = computed(() => {
    const horizon = ['Текущие', '+1 мес', '+2 мес', '+3 мес', '+4 мес']
    const categories = ['Backend', 'Data', 'Frontend', 'Cloud', 'DevOps']
    const base = {
      Backend: 240,
      Data: 255,
      Frontend: 215,
      Cloud: 260,
      DevOps: 245,
    }
    const growth = {
      Backend: 2.5,
      Data: 3.2,
      Frontend: 2.0,
      Cloud: 3.5,
      DevOps: 2.8,
    }
    return categories.map((cat, idx) => ({
      name: `${cat}`,
      data: horizon.map((_, h) => Math.round((base[cat] ?? 220) + h * (growth[cat] ?? 2.5) + seededNoise(cat, h, 2.2))),
    }))
  })

  const forecastOptions = computed(() => ({
    chart: { type: 'line', stacked: false, toolbar: { show: false } },
    stroke: { curve: 'smooth', width: 2 },
    colors: ['#dc3545', '#6c757d', '#495057', '#adb5bd', '#ced4da'],
    dataLabels: { enabled: false },
    legend: {
      position: 'top',
      horizontalAlign: 'left',
      fontSize: '11px',
      labels: { colors: '#6c757d' },
      markers: { radius: 5 },
      itemMargin: { horizontal: 10 },
    },
    xaxis: {
      categories: ['Текущие', '+1 мес', '+2 мес', '+3 мес', '+4 мес'],
      axisBorder: { show: true, color: '#e9ecef' },
      axisTicks: { show: false },
      labels: { style: { colors: '#6c757d' } },
    },
    yaxis: {
      labels: {
        formatter: (val) => `${val} т.р.`,
        style: { colors: '#6c757d' },
      },
    },
    grid: {
      borderColor: '#f1f3f5',
      strokeDashArray: 4,
    },
    tooltip: {
      shared: true,
      intersect: false,
      y: { formatter: (val) => `${val} т.р.` },
    },
    title: { text: '' },
  }))

  const sections = computed(() => [
    {
      id: 'technologies',
      icon: CircuitBoard,
      title: 'Карта технологий',
      description:
        'Управляйте технологическим стеком, синонимами и связями технологий между собой.',
      routeName: 'CompetenceCoreTechnologies',
      accentClass: 'cc-dashboard-card-accent-tech',
      badge: 'Технологии',
    },
    {
      id: 'competences',
      icon: BadgeCheck,
      title: 'Компетенции',
      description:
        'Описывайте компетенции, связывайте их с технологиями и профилями вакансий.',
      routeName: 'CompetenceCoreCompetences',
      accentClass: 'cc-dashboard-card-accent-competences',
      badge: 'Компетенции',
    },
    {
      id: 'vacancy-profiles',
      icon: BriefcaseBusiness,
      title: 'Профили вакансий',
      description:
        'Формируйте профили вакансий на основе компетенций и технологий для подбора специалистов.',
      routeName: 'CompetenceCoreVacancyProfiles',
      accentClass: 'cc-dashboard-card-accent-vacancies',
      badge: 'Профили вакансий',
    },
  ])

  const goTo = (routeName) => {
    if (!routeName) return
    router.push({ name: routeName })
  }

  return {
    LayoutDashboard,
    sections,
    kpis,
    periods,
    selectedPeriod,
    setPeriod,
    techPool,
    selectedTechnologies,
    toggleTechnology,
    categoryPool,
    selectedCategories,
    toggleCategory,
    popularityTrendSeries,
    popularityTrendOptions,
    categoryStackedSeries,
    categoryStackedOptions,
    topTechnologiesSeries,
    topTechnologiesOptions,
    levelSeries,
    levelOptions,
    topTechnologies,
    growthSignals,
    highlights,
    comparisonSeries,
    comparisonOptions,
    forecastSeries,
    forecastOptions,
    goTo,
  }
}


