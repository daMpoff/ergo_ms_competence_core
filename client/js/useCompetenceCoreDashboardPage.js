import { computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  LayoutDashboard,
  CircuitBoard,
  BadgeCheck,
  BriefcaseBusiness,
} from 'lucide-vue-next'

export function useCompetenceCoreDashboardPage() {
  const router = useRouter()

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
    goTo,
  }
}


