<template>
  <div class="container py-4" v-if="!loading && item">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-3">
      <div>
        <h2 class="mb-1">{{ item.name }}</h2>
        <div class="text-muted">
          <span v-if="item.level_display">Уровень: {{ item.level_display }}</span>
          <span v-if="item.is_core" class="ms-2 badge bg-success">Ключевая компетенция</span>
        </div>
      </div>
      <div class="mt-3 mt-md-0 text-md-end">
        <div>Популярность: <strong>{{ item.popularity }}</strong></div>
        <div>Релевантность: <strong>{{ (item.relevance ?? 0).toFixed(2) }}</strong></div>
      </div>
    </div>

    <p v-if="item.description" class="mb-4">
      {{ item.description }}
    </p>

    <h5 class="mb-3">
      Компоненты компетенции
      <span class="badge bg-secondary ms-2">{{ componentsCount }}</span>
    </h5>

    <div v-if="componentsCount === 0" class="alert alert-info">
      Компоненты для этой компетенции ещё не заданы.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-sm table-hover align-middle">
        <thead>
          <tr>
            <th>Умение</th>
            <th class="d-none d-lg-table-cell">Технология</th>
            <th class="text-center">Важность</th>
            <th class="text-center d-none d-md-table-cell">Уровень</th>
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
              <div v-if="comp.skill_technology_info">
                <div>{{ comp.skill_technology_info.technology_name }}</div>
                <div class="text-muted small">
                  Категория: {{ comp.skill_technology_info.technology_category }}
                </div>
              </div>
              <span v-else class="text-muted small">Без технологии</span>
            </td>
            <td class="text-center">
              {{ (comp.importance ?? 0).toFixed(2) }}
            </td>
            <td class="text-center d-none d-md-table-cell">
              <span v-if="comp.required_level_display" class="badge bg-light text-dark">
                {{ comp.required_level_display }}
              </span>
            </td>
            <td class="text-center d-none d-md-table-cell">
              {{ (comp.weight ?? 0).toFixed(2) }}
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
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCompetenceDetail } from '../js/useCompetences.js'

const route = useRoute()
const { item, loading, error, fetchCompetence } = useCompetenceDetail()

const componentsCount = computed(() => item.value?.components_count ?? item.value?.components?.length ?? 0)

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    fetchCompetence(id)
  }
})
</script>


