<template>
  <div class="container py-4" v-if="!loading && item">
    <div class="cc-detail-header d-flex flex-column flex-md-row justify-content-between align-items-md-start mb-3 gap-2">
      <div class="d-flex flex-column gap-2">
        <h2 class="mb-0">{{ item.name }}</h2>
        <div class="cc-detail-meta d-flex flex-wrap gap-2 align-items-center">
          <span v-if="item.level_display" class="badge cc-badge-level">
            {{ item.level_display }}
          </span>
          <span
            class="badge cc-badge-type"
            :class="item.is_core ? 'cc-badge-type-base' : 'cc-badge-type-narrow'"
          >
            <component :is="item.is_core ? Shield : Flame" :size="12" />
            {{ item.is_core ? 'Базовая' : 'Узконаправленная' }}
          </span>
          <span class="cc-detail-t-profile text-muted small">
            <strong>Положение в T‑профиле:</strong>
            {{ item.is_core ? 'горизонтальная база' : 'вертикальная специализация' }}
          </span>
        </div>
        <div v-if="tags.length" class="cc-detail-tags d-flex flex-wrap gap-1">
          <span
            v-for="tag in tags"
            :key="tag"
            class="badge cc-competence-tag"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12 col-lg-8">
        <div class="card shadow-sm border-0 h-100 cc-description-card">
          <div class="card-body">
            <h5 class="card-title">Формализованное описание компетенции</h5>
            <p v-if="item.description" class="mb-2">{{ item.description }}</p>
            <p v-else class="text-muted mb-2">Нет описания.</p>

            <div v-if="item.domains?.length" class="mb-2">
              <div class="text-muted small mb-1">Типовые области применения</div>
              <div class="d-flex flex-wrap gap-1">
                <span
                  v-for="domain in item.domains"
                  :key="domain"
                  class="badge bg-light text-dark"
                >
                  {{ domain }}
                </span>
              </div>
            </div>

            <div class="row g-2" v-if="item.prof_standards?.length || item.fgos_codes?.length">
              <div class="col-12 col-md-6" v-if="item.prof_standards?.length">
                <div class="text-muted small mb-1">Профстандарты</div>
                <ul class="list-unstyled mb-0 small">
                  <li v-for="ps in item.prof_standards" :key="ps">• {{ ps }}</li>
                </ul>
              </div>
              <div class="col-12 col-md-6" v-if="item.fgos_codes?.length">
                <div class="text-muted small mb-1">ФГОС</div>
                <ul class="list-unstyled mb-0 small">
                  <li v-for="fg in item.fgos_codes" :key="fg">• {{ fg }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0 h-100 cc-kpi-panel">
          <div class="card-body d-flex flex-column gap-3">
            <div class="cc-kpi-grid">
              <div class="cc-kpi-card cc-kpi-card--compact">
                <span class="cc-kpi-icon"><Layers :size="16" /></span>
                <div>
                  <div class="cc-kpi-label">Компонентов</div>
                  <div class="cc-kpi-value">{{ componentsCount }}</div>
                </div>
              </div>
              <div class="cc-kpi-card cc-kpi-card--compact">
                <span class="cc-kpi-icon"><Grid3x3 :size="16" /></span>
                <div>
                  <div class="cc-kpi-label">Категории умений</div>
                  <div class="cc-kpi-value">{{ matrixRows.length }}</div>
                </div>
              </div>
              <div class="cc-kpi-card cc-kpi-card--compact">
                <span class="cc-kpi-icon"><TrendingUp :size="16" /></span>
                <div>
                  <div class="cc-kpi-label">Популярность</div>
                  <div class="cc-kpi-value">{{ item.popularity }}%</div>
                </div>
              </div>
              <div class="cc-kpi-card cc-kpi-card--compact">
                <span class="cc-kpi-icon"><Gauge :size="16" /></span>
                <div>
                  <div class="cc-kpi-label">Релевантность</div>
                  <div class="cc-kpi-value">{{ (item.relevance ?? 0).toFixed(2) }}</div>
                </div>
              </div>
            </div>

            
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12 col-lg-8">
        <div class="card shadow-sm border-0 h-100 cc-competence-matrix-card">
          <div class="card-body">
            <h5 class="card-title mb-2">Матрица умений по таксономии Блума</h5>
            <p class="text-muted small mb-3">
              Отражает распределение умений в компетенции по категориям и уровням таксономии Блума
            </p>

            <div v-if="matrixRows.length === 0" class="text-muted small">
              Недостаточно данных для построения матрицы — добавьте хотя бы один компонент компетенции.
            </div>

            <div v-else class="table-responsive">
              <table class="table table-sm align-middle cc-competence-matrix-table">
                <thead>
                  <tr>
                    <th>Категория умения</th>
                    <th
                      v-for="level in levelColumns"
                      :key="level"
                      class="text-center"
                    >
                      {{ level }}
                    </th>
                    <th class="text-center">Всего</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in matrixRows" :key="row.category">
                    <td>
                      <div class="fw-semibold">{{ row.category }}</div>
                    </td>
                    <td
                      v-for="level in levelColumns"
                      :key="level"
                      class="text-center"
                    >
                      <div class="cc-competence-matrix-cell">
                        <span class="cc-competence-matrix-count">
                          {{ row.levels[level] }}
                          <span
                            v-if="row.total > 0 && row.levels[level] > 0"
                            class="text-muted"
                          >
                            ({{ ((row.levels[level] / row.total) * 100).toFixed(0) }}%)
                          </span>
                        </span>
                        <div class="cc-competence-matrix-bar-wrapper">
                          <div
                            class="cc-competence-matrix-bar"
                            :style="{ width: row.max > 0 ? `${(row.levels[level] / row.max) * 100}%` : '0%' }"
                          ></div>
                        </div>
                      </div>
                    </td>
                    <td class="text-center">
                      <strong>{{ row.total }}</strong>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0 h-100 cc-competence-designer">
          <div class="card-body">
            <h5 class="card-title mb-2">Добавить компонент компетенции</h5>

            <div class="mb-2">
              <label class="form-label small text-muted">Умение</label>
              <input
                v-model="draftComponent.skill_name"
                type="text"
                class="form-control form-control-sm"
                placeholder="Например, Проектирование API"
              />
            </div>

            <div class="mb-2">
              <label class="form-label small text-muted">Категория умения</label>
              <input
                v-model="draftComponent.skill_category"
                type="text"
                class="form-control form-control-sm"
                placeholder="Architecture, Database, Integration..."
              />
            </div>

            <div class="row g-2 mb-2">
              <div class="col-6">
                <label class="form-label small text-muted">Уровень</label>
                <select
                  v-model="draftComponent.required_level_display"
                  class="form-select form-select-sm"
                >
                  <option value="Junior">Начинающий</option>
                  <option value="Middle">Средний</option>
                  <option value="Senior">Опытный</option>
                  <option value="Expert">Экспертный</option>
                </select>
              </div>
              <div class="col-6">
                <label class="form-label small text-muted">Важность (0–1)</label>
                <input
                  v-model.number="draftComponent.importance"
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  class="form-control form-control-sm"
                />
              </div>
            </div>

            <div class="row g-2 mb-2">
              <div class="col-6">
                <label class="form-label small text-muted">Вес (0–1)</label>
                <input
                  v-model.number="draftComponent.weight"
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  class="form-control form-control-sm"
                />
              </div>
              <div class="col-6">
                <label class="form-label small text-muted">Технология</label>
                <input
                  v-model="draftComponent.technology_name"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Django, Celery, PostgreSQL..."
                />
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label small text-muted">Категория технологии</label>
              <input
                v-model="draftComponent.technology_category"
                type="text"
                class="form-control form-control-sm"
                placeholder="Backend, Async, Database..."
              />
            </div>

            <div class="d-flex justify-content-between align-items-center mt-2">
              <button
                type="button"
                class="btn btn-outline-secondary btn-sm"
                @click="resetDraftComponent"
              >
                Очистить
              </button>
              <button
                type="button"
                class="btn btn-danger btn-sm"
                :disabled="!canAddComponent"
                @click="addComponent"
              >
                Добавить компонент
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <h5 class="mb-3 d-flex align-items-center gap-2 cc-components-header">
      <span class="cc-components-title">Компоненты компетенции</span>
      <span class="badge cc-badge-count">{{ componentsCount }}</span>
      <span v-if="componentsCount === 0" class="text-muted small">Добавьте первый компонент</span>
    </h5>

    <div v-if="componentsCount === 0" class="alert alert-info">
      Компоненты для этой компетенции ещё не заданы.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-sm table-hover align-middle cc-components-table">
        <thead>
          <tr>
            <th>Умение</th>
            <th class="d-none d-lg-table-cell">Технология</th>
            <th class="text-center">Важность</th>
            <th class="text-center d-none d-md-table-cell">Уровень</th>
            <th class="text-center d-none d-md-table-cell">Уровень Блума</th>
            <th class="text-center d-none d-md-table-cell">Вес</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comp in item.components" :key="comp.id">
            <td>
              <div class="fw-semibold">
                {{ comp.skill_name }}
              </div>
              <div class="text-muted small">
                Категория: {{ comp.skill_category }}
              </div>
            </td>
            <td class="d-none d-lg-table-cell">
              <div v-if="comp.skill_technology_info" class="cc-tech-badge">
                <div class="fw-semibold small">{{ comp.skill_technology_info.technology_name }}</div>
                <div class="text-muted small">
                  Категория: {{ comp.skill_technology_info.technology_category }}
                </div>
              </div>
              <span v-else class="text-muted small">Без технологии</span>
            </td>
            <td class="text-center">
              <div class="cc-cell-metric">
                <span class="cc-metric-value">{{ (comp.importance ?? 0).toFixed(2) }}</span>
                <div class="cc-metric-bar">
                  <div
                    class="cc-metric-bar-fill"
                    :style="{ width: `${Math.min(Math.max((comp.importance ?? 0) * 100, 0), 100)}%` }"
                  ></div>
                </div>
              </div>
            </td>
            <td class="text-center d-none d-md-table-cell">
              <span
                v-if="comp.required_level_display"
                class="badge cc-badge-level cc-badge-level--compact"
              >
                {{ comp.required_level_display }}
              </span>
            </td>
            <td class="text-center d-none d-md-table-cell">
              <span v-if="comp.bloom_level" :class="bloomLevelClass(comp.bloom_level)">
                {{ comp.bloom_level }}
              </span>
            </td>
            <td class="text-center d-none d-md-table-cell">
              <div class="cc-cell-metric">
                <span class="cc-metric-value">{{ (comp.weight ?? 0).toFixed(2) }}</span>
                <div class="cc-metric-bar cc-metric-bar--muted">
                  <div
                    class="cc-metric-bar-fill"
                    :style="{ width: `${Math.min(Math.max((comp.weight ?? 0) * 100, 0), 100)}%` }"
                  ></div>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div v-else-if="loading" class="container py-5 text-center">
    Загрузка...
  </div>

  <div v-else-if="error" class="container py-5">
    <div class="alert alert-danger">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'
import { Flame, Gauge, Grid3x3, Layers, Shield, TrendingUp } from 'lucide-vue-next'
import { useCompetenceDetail } from '../js/useCompetences.js'

const route = useRoute()
const toast = useToast()
const { item, loading, error, fetchCompetence } = useCompetenceDetail()

const componentsCount = computed(
  () => item.value?.components_count ?? item.value?.components?.length ?? 0,
)

const tags = computed(() => item.value?.tags || [])

const levelColumns = ['Запоминание', 'Понимание', 'Применение', 'Анализ', 'Оценка', 'Создание']

const matrixRows = computed(() => {
  const components = item.value?.components || []
  if (!components.length) {
    return []
  }

  const map = new Map()

  components.forEach((comp) => {
    const category = comp.skill_category || 'Без категории'
    if (!map.has(category)) {
      const levels = {}
      levelColumns.forEach((lvl) => {
        levels[lvl] = 0
      })
      map.set(category, {
        category,
        levels,
        total: 0,
        max: 0,
      })
    }
    const row = map.get(category)
    const sourceLevel = comp.bloom_level || 'Понимание'
    const normalizedLevel = levelColumns.includes(sourceLevel) ? sourceLevel : 'Понимание'
    row.levels[normalizedLevel] += 1
    row.total += 1
    row.max = Math.max(row.max, row.levels[normalizedLevel])
  })

  return Array.from(map.values())
})

const bloomLevelsSummary = computed(() => {
  const components = item.value?.components || []
  if (!components.length) {
    return '—'
  }
  const order = ['Запоминание', 'Понимание', 'Применение', 'Анализ', 'Оценка', 'Создание']
  const counts = new Map()
  components.forEach((comp) => {
    const level = comp.bloom_level
    if (!level) return
    counts.set(level, (counts.get(level) || 0) + 1)
  })
  if (!counts.size) {
    return '—'
  }
  return order
    .filter((lvl) => counts.has(lvl))
    .map((lvl) => `${lvl.toLowerCase()} — ${counts.get(lvl)}`)
    .join(', ')
})

const draftComponent = ref(createEmptyDraftComponent())

function createEmptyDraftComponent() {
  return {
    skill_name: '',
    skill_category: '',
    required_level_display: 'Middle',
    importance: 0.8,
    weight: 0.3,
    technology_name: '',
    technology_category: '',
  }
}

const resetDraftComponent = () => {
  draftComponent.value = createEmptyDraftComponent()
}

const canAddComponent = computed(() => {
  return !!draftComponent.value.skill_name && !!draftComponent.value.skill_category
})

const bloomLevelClass = (level) => {
  const map = {
    Запоминание: 'remember',
    Понимание: 'understand',
    Применение: 'apply',
    Анализ: 'analyze',
    Оценка: 'evaluate',
    Создание: 'create',
  }
  const key = map[level] || 'default'
  return ['badge', 'cc-badge-bloom', `cc-badge-bloom--${key}`]
}

const bloomLevelTags = computed(() => {
  const components = item.value?.components || []
  if (!components.length) return []
  const order = [
    { label: 'Запоминание', key: 'remember' },
    { label: 'Понимание', key: 'understand' },
    { label: 'Применение', key: 'apply' },
    { label: 'Анализ', key: 'analyze' },
    { label: 'Оценка', key: 'evaluate' },
    { label: 'Создание', key: 'create' },
  ]
  const counts = new Map()
  components.forEach((comp) => {
    if (!comp.bloom_level) return
    counts.set(comp.bloom_level, (counts.get(comp.bloom_level) || 0) + 1)
  })
  return order
    .filter(({ label }) => counts.has(label))
    .map(({ label, key }) => ({ label, key, count: counts.get(label) }))
})

const addComponent = () => {
  if (!item.value) {
    return
  }

  if (!canAddComponent.value) {
    toast.warning('Заполните наименование и категорию умения')
    return
  }

  const components = Array.isArray(item.value.components) ? item.value.components : []
  const nextId =
    (components.reduce(
      (maxId, comp) => Math.max(maxId, Number(comp.id) || 0),
      0,
    ) || 0) + 1

  const newComponent = {
    id: nextId,
    skill_name: draftComponent.value.skill_name,
    skill_category: draftComponent.value.skill_category,
    importance: Number(draftComponent.value.importance) || 0,
    required_level_display: draftComponent.value.required_level_display,
    weight: Number(draftComponent.value.weight) || 0,
    skill_technology_info: draftComponent.value.technology_name
      ? {
          technology_name: draftComponent.value.technology_name,
          technology_category: draftComponent.value.technology_category || 'Без категории',
        }
      : null,
  }

  const updated = [...components, newComponent]
  item.value = {
    ...item.value,
    components: updated,
    components_count: updated.length,
  }

  toast.success('Компонент добавлен (демо-режим, без сохранения в БД)')
  resetDraftComponent()
}

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    fetchCompetence(id)
  }
})
</script>

<style scoped src="../scss/CompetenceDetailPage.scss"></style>

