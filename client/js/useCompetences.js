import { ref } from 'vue'
import { apiClient } from '@/js/api/manager'
import { endpoints } from '@/js/api/endpoints'

export function useCompetencesList() {
  const items = ref([])
  const loading = ref(false)
  const error = ref('')

  const mockItems = [
    {
      id: 1,
      name: 'Backend разработка',
      description: 'Проектирование и поддержка REST/GraphQL API, интеграции с внешними системами, работа с БД.',
      level_display: 'Middle',
      is_core: false,
      popularity: 87,
      relevance: 0.82,
      tags: ['Python', 'Django', 'REST', 'PostgreSQL', 'Celery'],
    },
    {
      id: 2,
      name: 'Data Engineering',
      description: 'Проектирование конвейеров данных (batch/stream), витрины, качество и каталогизация данных.',
      level_display: 'Senior',
      is_core: true,
      popularity: 78,
      relevance: 0.81,
      tags: ['ETL', 'Kafka', 'Airflow', 'DWH', 'SQL'],
    },
    {
      id: 3,
      name: 'Frontend (Vue)',
      description: 'Разработка SPA, дизайн-системы, маршрутизация, state-management, интеграция с API.',
      level_display: 'Middle',
      is_core: false,
      popularity: 72,
      relevance: 0.76,
      tags: ['Vue', 'TypeScript', 'UI Kit', 'REST'],
    },
    {
      id: 4,
      name: 'DevOps / SRE',
      description: 'CI/CD, инфраструктура как код, мониторинг и поддержка доступности сервисов.',
      level_display: 'Senior',
      is_core: true,
      popularity: 70,
      relevance: 0.79,
      tags: ['Docker', 'Kubernetes', 'CI/CD', 'Prometheus', 'Grafana'],
    },
    {
      id: 5,
      name: 'Системный анализ',
      description: 'Сбор требований, моделирование процессов, постановка задач команде разработки.',
      level_display: 'Middle',
      is_core: true,
      popularity: 65,
      relevance: 0.73,
      tags: ['BPMN', 'UML', 'User Stories'],
    },
    {
      id: 6,
      name: 'Тестирование (QA Automation)',
      description: 'Проектирование автотестов, поддержка тестового фреймворка, интеграция в CI/CD.',
      level_display: 'Middle',
      is_core: true,
      popularity: 69,
      relevance: 0.77,
      tags: ['Pytest', 'Playwright', 'CI/CD', 'API testing'],
    },
    {
      id: 7,
      name: 'Продуктовый менеджмент',
      description: 'Формирование бэклога, работа с метриками продукта, управление приоритетами и релизами.',
      level_display: 'Senior',
      is_core: true,
      popularity: 61,
      relevance: 0.74,
      tags: ['Roadmap', 'A/B tests', 'Product Metrics'],
    },
    {
      id: 8,
      name: 'UX / UI дизайн',
      description: 'Проектирование пользовательских сценариев, создание макетов и дизайн-системы.',
      level_display: 'Middle',
      is_core: false,
      popularity: 58,
      relevance: 0.72,
      tags: ['Figma', 'Design System', 'User Research'],
    },
    {
      id: 9,
      name: 'MLOps',
      description: 'Построение пайплайнов обучения и выката ML-моделей, мониторинг качества и деградаций.',
      level_display: 'Senior',
      is_core: false,
      popularity: 64,
      relevance: 0.78,
      tags: ['MLFlow', 'Kafka', 'Docker', 'Monitoring'],
    },
    {
      id: 10,
      name: 'Информационная безопасность',
      description: 'Анализ уязвимостей, безопасная разработка, контроль доступа и управление инцидентами.',
      level_display: 'Senior',
      is_core: false,
      popularity: 59,
      relevance: 0.75,
      tags: ['OWASP', 'Threat Modeling', 'SIEM'],
    },
  ]

  const fetchCompetences = async (params = {}) => {
    loading.value = true
    error.value = ''
    try {
      const resp = await apiClient.get(endpoints.competenceCore.competencesList, params)
      const data = resp.data
      const results = Array.isArray(data) ? data : data.results ?? []
      if (!results || results.length === 0) {
        // Если API вернул пустой список – используем шаблонные данные,
        // чтобы витрина компетенций всегда была наполнена.
        items.value = mockItems
      } else {
        items.value = results
      }
    } catch (e) {
      console.error('Ошибка загрузки компетенций', e)
      // Заглушка: используем условные данные, чтобы страницы работали без БД
      items.value = mockItems
      error.value = ''
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    error,
    fetchCompetences,
  }
}

export function useCompetenceDetail() {
  const item = ref(null)
  const loading = ref(false)
  const error = ref('')

  const mockDetailsById = {
    1: {
      id: 1,
      name: 'Backend разработка',
      description: 'Проектирование и поддержка backend-сервисов: REST/GraphQL, очереди, кеши, реляционные и нереляционные БД.',
      level_display: 'Middle',
      is_core: false,
      profile_type: 'Узконаправленная компетенция в области backend‑разработки',
      prof_standards: ['Программист', 'Разработчик программного обеспечения'],
      fgos_codes: ['09.03.04 Программная инженерия', '09.03.01 Информатика и вычислительная техника'],
      domains: ['Веб-разработка', 'Интеграционные решения', 'Внутренние корпоративные системы'],
      popularity: 87,
      relevance: 0.82,
      components_count: 15,
      components: [
        { id: 101, skill_name: 'Проектирование REST/GraphQL API', skill_category: 'Архитектура и интеграции', importance: 0.9, required_level_display: 'Middle', weight: 0.18, bloom_level: 'Создание', skill_technology_info: { technology_name: 'Django / DRF', technology_category: 'Backend' } },
        { id: 102, skill_name: 'Контракт API, версионирование и backward compatibility', skill_category: 'Архитектура и интеграции', importance: 0.85, required_level_display: 'Middle', weight: 0.11, bloom_level: 'Создание', skill_technology_info: { technology_name: 'OpenAPI / Swagger', technology_category: 'Documentation' } },
        { id: 103, skill_name: 'Асинхронные очереди и ретраи задач', skill_category: 'Архитектура и интеграции', importance: 0.82, required_level_display: 'Middle', weight: 0.1, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Celery / RabbitMQ', technology_category: 'Async' } },
        { id: 104, skill_name: 'Транзакции и изоляция', skill_category: 'Хранение и доступ к данным', importance: 0.8, required_level_display: 'Middle', weight: 0.09, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'PostgreSQL', technology_category: 'Database' } },
        { id: 105, skill_name: 'Оптимизация запросов и индексация', skill_category: 'Хранение и доступ к данным', importance: 0.78, required_level_display: 'Middle', weight: 0.09, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'PostgreSQL', technology_category: 'Database' } },
        { id: 106, skill_name: 'Кеширование и консистентность', skill_category: 'Производительность', importance: 0.76, required_level_display: 'Middle', weight: 0.08, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Redis', technology_category: 'Cache' } },
        { id: 107, skill_name: 'API gateway и маршрутизация трафика', skill_category: 'Архитектура и интеграции', importance: 0.72, required_level_display: 'Middle', weight: 0.07, bloom_level: 'Понимание', skill_technology_info: { technology_name: 'Nginx / Traefik', technology_category: 'Gateway' } },
        { id: 108, skill_name: 'Тестирование API (юнит и интеграционное)', skill_category: 'Качество', importance: 0.7, required_level_display: 'Middle', weight: 0.07, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Pytest / Postman', technology_category: 'Testing' } },
        { id: 109, skill_name: 'Наблюдаемость: метрики, логи, трассировки', skill_category: 'Наблюдаемость и устойчивость', importance: 0.72, required_level_display: 'Middle', weight: 0.08, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Sentry / Prometheus', technology_category: 'Monitoring' } },
        { id: 110, skill_name: 'Безопасность API и контроль доступа', skill_category: 'Безопасность', importance: 0.7, required_level_display: 'Middle', weight: 0.07, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'OWASP / JWT', technology_category: 'Security' } },
        { id: 111, skill_name: 'Работа с файловым и объектным хранением', skill_category: 'Хранение и доступ к данным', importance: 0.62, required_level_display: 'Middle', weight: 0.06, bloom_level: 'Применение', skill_technology_info: { technology_name: 'S3-хранилища', technology_category: 'Storage' } },
        { id: 112, skill_name: 'Секционирование и шардирование', skill_category: 'Хранение и доступ к данным', importance: 0.64, required_level_display: 'Middle', weight: 0.06, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'PostgreSQL', technology_category: 'Database' } },
        { id: 113, skill_name: 'CI/CD для сервисов и миграций', skill_category: 'Качество', importance: 0.6, required_level_display: 'Middle', weight: 0.05, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Alembic / Django migrations', technology_category: 'Migrations' } },
        { id: 114, skill_name: 'Резервное копирование и восстановление', skill_category: 'Наблюдаемость и устойчивость', importance: 0.58, required_level_display: 'Middle', weight: 0.04, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Backup/Restore', technology_category: 'Resilience' } },
        { id: 115, skill_name: 'Управление конфигурациями и секретами', skill_category: 'Безопасность', importance: 0.56, required_level_display: 'Middle', weight: 0.04, bloom_level: 'Понимание', skill_technology_info: { technology_name: 'Vault / Env', technology_category: 'Security' } },
      ],
    },
    2: {
      id: 2,
      name: 'Data Engineering',
      description: 'Построение надёжных конвейеров и витрин данных, обеспечение качества и доступности данных для бизнеса.',
      level_display: 'Senior',
      is_core: false,
      profile_type: 'Узконаправленная компетенция в области инженерии данных',
      prof_standards: ['Специалист по анализу и обработке данных'],
      fgos_codes: ['09.03.03 Прикладная информатика', '27.03.05 Инноватика (профиль «Цифровая трансформация»)'],
      domains: ['Хранилища данных и BI', 'Финансовая аналитика', 'Операционная аналитика'],
      popularity: 78,
      relevance: 0.81,
      components_count: 15,
      components: [
        { id: 201, skill_name: 'Проектирование DWH и витрин под BI', skill_category: 'Архитектура данных', importance: 0.9, required_level_display: 'Senior', weight: 0.14, bloom_level: 'Создание', skill_technology_info: { technology_name: 'Star / Snowflake schema', technology_category: 'Data Warehouse' } },
        { id: 202, skill_name: 'Batch- и stream-конвейеры', skill_category: 'Конвейеры данных', importance: 0.86, required_level_display: 'Senior', weight: 0.12, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Airflow / Kafka', technology_category: 'Data Pipelines' } },
        { id: 203, skill_name: 'Качество и валидация данных', skill_category: 'Качество данных', importance: 0.82, required_level_display: 'Senior', weight: 0.1, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'Great Expectations', technology_category: 'Data Quality' } },
        { id: 204, skill_name: 'Оптимизация SQL и индексация', skill_category: 'Хранение и доступ к данным', importance: 0.8, required_level_display: 'Senior', weight: 0.1, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'PostgreSQL', technology_category: 'Database' } },
        { id: 205, skill_name: 'Оркестрация и мониторинг конвейеров', skill_category: 'Наблюдаемость и устойчивость', importance: 0.76, required_level_display: 'Senior', weight: 0.09, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Airflow / Prometheus', technology_category: 'Orchestration' } },
        { id: 206, skill_name: 'Моделирование витрин под аналитиков', skill_category: 'Архитектура данных', importance: 0.78, required_level_display: 'Senior', weight: 0.08, bloom_level: 'Создание', skill_technology_info: { technology_name: 'PowerBI / Tableau', technology_category: 'BI' } },
        { id: 207, skill_name: 'Каталогизация и метаданные', skill_category: 'Качество данных', importance: 0.72, required_level_display: 'Senior', weight: 0.07, bloom_level: 'Понимание', skill_technology_info: { technology_name: 'Data Catalog', technology_category: 'Data Governance' } },
        { id: 208, skill_name: 'Распределённая обработка данных', skill_category: 'Конвейеры данных', importance: 0.74, required_level_display: 'Senior', weight: 0.07, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Spark / Flink', technology_category: 'Distributed Processing' } },
        { id: 209, skill_name: 'Надёжность пайплайнов и SLA', skill_category: 'Наблюдаемость и устойчивость', importance: 0.7, required_level_display: 'Senior', weight: 0.06, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Alerting / SLA', technology_category: 'Reliability' } },
        { id: 210, skill_name: 'Тестирование данных и схем', skill_category: 'Качество данных', importance: 0.68, required_level_display: 'Senior', weight: 0.06, bloom_level: 'Применение', skill_technology_info: { technology_name: 'DBT tests / Pytest', technology_category: 'Testing' } },
        { id: 211, skill_name: 'Управление схемами и миграциями', skill_category: 'Хранение и доступ к данным', importance: 0.65, required_level_display: 'Senior', weight: 0.05, bloom_level: 'Применение', skill_technology_info: { technology_name: 'DBT / Liquibase', technology_category: 'Migrations' } },
        { id: 212, skill_name: 'Data Lineage и аудит', skill_category: 'Качество данных', importance: 0.64, required_level_display: 'Senior', weight: 0.05, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'OpenLineage', technology_category: 'Governance' } },
        { id: 213, skill_name: 'Пропускная способность и QoS', skill_category: 'Конвейеры данных', importance: 0.62, required_level_display: 'Senior', weight: 0.05, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Kafka quotas / QoS', technology_category: 'Streaming' } },
        { id: 214, skill_name: 'Безопасность и доступы к данным', skill_category: 'Безопасность', importance: 0.6, required_level_display: 'Senior', weight: 0.04, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Row-Level Security / IAM', technology_category: 'Security' } },
        { id: 215, skill_name: 'Финансовая эффективность хранения и вычислений', skill_category: 'Наблюдаемость и устойчивость', importance: 0.58, required_level_display: 'Senior', weight: 0.04, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'Cost monitoring', technology_category: 'FinOps' } },
      ],
    },
    3: {
      id: 3,
      name: 'Frontend (Vue)',
      description: 'Разработка клиентских приложений на Vue: дизайн-система, маршрутизация, работа с API и состоянием.',
      level_display: 'Middle',
      is_core: false,
      profile_type: 'Узконаправленная компетенция (вертикальная часть T‑профиля)',
      prof_standards: ['Веб-разработчик', 'Инженер по разработке пользовательских интерфейсов'],
      fgos_codes: ['09.03.02 Информационные системы и технологии'],
      domains: ['SPA/SPA+SSR приложения', 'Личный кабинет и админ‑интерфейсы', 'Внутренние UI‑платформы'],
      popularity: 72,
      relevance: 0.76,
      components_count: 15,
      components: [
        { id: 301, skill_name: 'Проектирование компонентов и дизайн-системы', skill_category: 'Архитектура интерфейса', importance: 0.84, required_level_display: 'Middle', weight: 0.12, bloom_level: 'Создание', skill_technology_info: { technology_name: 'Vue 3 / Design System', technology_category: 'Frontend' } },
        { id: 302, skill_name: 'Маршрутизация и защита маршрутов', skill_category: 'Архитектура интерфейса', importance: 0.8, required_level_display: 'Middle', weight: 0.1, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Vue Router', technology_category: 'Frontend' } },
        { id: 303, skill_name: 'Управление состоянием', skill_category: 'Архитектура интерфейса', importance: 0.78, required_level_display: 'Middle', weight: 0.1, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'Pinia / Vuex', technology_category: 'Frontend' } },
        { id: 304, skill_name: 'Интеграция с API и обработка ошибок', skill_category: 'Интеграции', importance: 0.76, required_level_display: 'Middle', weight: 0.1, bloom_level: 'Применение', skill_technology_info: { technology_name: 'REST / Axios', technology_category: 'Integration' } },
        { id: 305, skill_name: 'Тестирование интерфейсов', skill_category: 'Качество', importance: 0.7, required_level_display: 'Middle', weight: 0.1, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Vitest / Testing Library', technology_category: 'Testing' } },
        { id: 306, skill_name: 'Доступность (a11y)', skill_category: 'Качество', importance: 0.72, required_level_display: 'Middle', weight: 0.08, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'WCAG / Axe', technology_category: 'Accessibility' } },
        { id: 307, skill_name: 'Микроанимации и обратная связь', skill_category: 'UX', importance: 0.64, required_level_display: 'Middle', weight: 0.07, bloom_level: 'Применение', skill_technology_info: { technology_name: 'CSS / Motion', technology_category: 'UI/UX' } },
        { id: 308, skill_name: 'SSR / SSG рендеринг', skill_category: 'Архитектура интерфейса', importance: 0.7, required_level_display: 'Middle', weight: 0.08, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'Nuxt', technology_category: 'Frontend' } },
        { id: 309, skill_name: 'Оптимизация бандла и производительность', skill_category: 'Производительность', importance: 0.74, required_level_display: 'Middle', weight: 0.08, bloom_level: 'Анализ', skill_technology_info: { technology_name: 'Vite / Webpack', technology_category: 'Performance' } },
        { id: 310, skill_name: 'Стили и дизайн-токены', skill_category: 'Архитектура интерфейса', importance: 0.68, required_level_display: 'Middle', weight: 0.06, bloom_level: 'Понимание', skill_technology_info: { technology_name: 'Design Tokens / SCSS', technology_category: 'Styling' } },
        { id: 311, skill_name: 'Формы и валидация', skill_category: 'Интеграции', importance: 0.66, required_level_display: 'Middle', weight: 0.06, bloom_level: 'Применение', skill_technology_info: { technology_name: 'VeeValidate / Custom forms', technology_category: 'Forms' } },
        { id: 312, skill_name: 'Состояние офлайн и кэш браузера', skill_category: 'Интеграции', importance: 0.62, required_level_display: 'Middle', weight: 0.06, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Service Worker / IndexedDB', technology_category: 'Offline' } },
        { id: 313, skill_name: 'Мультиязычность и локализация', skill_category: 'UX', importance: 0.6, required_level_display: 'Middle', weight: 0.05, bloom_level: 'Понимание', skill_technology_info: { technology_name: 'Vue I18n', technology_category: 'Localization' } },
        { id: 314, skill_name: 'Сбор и анализ метрик фронтенда', skill_category: 'Наблюдаемость и устойчивость', importance: 0.58, required_level_display: 'Middle', weight: 0.05, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Web Vitals / Sentry', technology_category: 'Monitoring' } },
        { id: 315, skill_name: 'UI тестирование end-to-end', skill_category: 'Качество', importance: 0.6, required_level_display: 'Middle', weight: 0.05, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Playwright / Cypress', technology_category: 'Testing' } },
        { id: 316, skill_name: 'Design Review и контроль консистентности UI', skill_category: 'Архитектура интерфейса', importance: 0.64, required_level_display: 'Middle', weight: 0.05, bloom_level: 'Оценка', skill_technology_info: { technology_name: 'Design Tokens / Figma', technology_category: 'Styling' } },
        { id: 317, skill_name: 'Таблицы и виртуализация списков', skill_category: 'Производительность', importance: 0.62, required_level_display: 'Middle', weight: 0.05, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Virtual Scrolling', technology_category: 'Performance' } },
        { id: 318, skill_name: 'Обработка ошибок и уведомлений UI', skill_category: 'UX', importance: 0.6, required_level_display: 'Middle', weight: 0.04, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Toast / Dialog patterns', technology_category: 'UI/UX' } },
        { id: 319, skill_name: 'Работа с графиками и визуализацией', skill_category: 'Интеграции', importance: 0.6, required_level_display: 'Middle', weight: 0.04, bloom_level: 'Применение', skill_technology_info: { technology_name: 'Chart libs', technology_category: 'Visualization' } },
        { id: 320, skill_name: 'Сборка, линтинг и форматирование', skill_category: 'Качество', importance: 0.58, required_level_display: 'Middle', weight: 0.04, bloom_level: 'Понимание', skill_technology_info: { technology_name: 'ESLint / Prettier', technology_category: 'Quality' } },
      ],
    },
  }

  const fetchCompetence = async (id) => {
    if (!id) return
    loading.value = true
    error.value = ''
    try {
      const endpoint = endpoints.competenceCore.competenceDetail(id)
      const resp = await apiClient.get(endpoint)
      item.value = resp.data
    } catch (e) {
      console.error('Ошибка загрузки компетенции', e)
      // Заглушка: используем условные данные
      const fallback = mockDetailsById[id] || mockDetailsById[1]
      item.value = { ...fallback, id }
      error.value = ''
    } finally {
      loading.value = false
    }
  }

  return {
    item,
    loading,
    error,
    fetchCompetence,
  }
}


