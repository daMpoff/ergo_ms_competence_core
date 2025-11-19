export default {
  // Главная страница блока компетенций и вакансий
  CompetenceCoreHome: {
    path: '/competence-core',
    component: '@/modules/competence_core/client/pages/KnowledgeBaseLayoutPage.vue',
    redirect: 'CompetenceCoreVacancyProfiles',
    meta: {
      title: 'Компетенции и вакансии',
      requiresAuth: true,
    },
  },

  // Список компетенций
  CompetenceCoreCompetences: {
    path: '/competence-core/competences',
    component: '@/modules/competence_core/client/pages/CompetencesListPage.vue',
    meta: {
      title: 'Компетенции',
      requiresAuth: true,
    },
  },

  // Детальная страница компетенции
  CompetenceCoreCompetenceDetail: {
    path: '/competence-core/competences/:id(\\d+)',
    component: '@/modules/competence_core/client/pages/CompetenceDetailPage.vue',
    meta: {
      title: 'Детали компетенции',
      requiresAuth: true,
    },
  },

  // Список профилей вакансий
  CompetenceCoreVacancyProfiles: {
    path: '/competence-core/vacancies',
    component: '@/modules/competence_core/client/pages/VacancyProfilesListPage.vue',
    meta: {
      title: 'Профили вакансий',
      requiresAuth: true,
    },
  },

  // Детальная страница профиля вакансии
  CompetenceCoreVacancyProfileDetail: {
    path: '/competence-core/vacancies/:id(\\d+)',
    component: '@/modules/competence_core/client/pages/VacancyProfileDetailPage.vue',
    meta: {
      title: 'Профиль вакансии',
      requiresAuth: true,
    },
  },

  // Список технологий (skill_map)
  CompetenceCoreTechnologies: {
    path: '/competence-core/technologies',
    component: '@/modules/competence_core/client/pages/TechnologiesListPage.vue',
    meta: {
      title: 'Технологии',
      requiresAuth: true,
    },
  },
}




