<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="mb-0">Компетенции</h2>
    </div>

    <div class="row mb-3 g-2">
      <div class="col-12 col-md-4">
        <input
          v-model="search"
          type="text"
          class="form-control"
          placeholder="Поиск по названию или описанию"
          @keyup.enter="reload"
        />
      </div>
      <div class="col-12 col-md-3">
        <select v-model="level" class="form-select" @change="reload">
          <option value="">Все уровни</option>
          <option value="JUNIOR">Junior</option>
          <option value="MIDDLE">Middle</option>
          <option value="SENIOR">Senior</option>
          <option value="EXPERT">Expert</option>
        </select>
      </div>
      <div class="col-12 col-md-2 d-flex">
        <button class="btn btn-primary w-100" @click="reload">
          Обновить
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      Загрузка...
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="items.length === 0" class="alert alert-info">
        Компетенции не найдены.
      </div>

      <div class="table-responsive" v-else>
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>Название</th>
              <th class="d-none d-md-table-cell">Уровень</th>
              <th class="d-none d-md-table-cell">Ключевая</th>
              <th class="text-end">Популярность</th>
              <th class="text-end d-none d-md-table-cell">Релевантность</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="comp in items" :key="comp.id">
              <td>
                <div class="fw-semibold">{{ comp.name }}</div>
                <div v-if="comp.description" class="text-muted small">
                  {{ comp.description }}
                </div>
              </td>
              <td class="d-none d-md-table-cell">
                <span v-if="comp.level_display" class="badge bg-secondary">
                  {{ comp.level_display }}
                </span>
              </td>
              <td class="d-none d-md-table-cell">
                <span
                  class="badge"
                  :class="comp.is_core ? 'bg-success' : 'bg-outline-secondary'"
                >
                  {{ comp.is_core ? 'Да' : 'Нет' }}
                </span>
              </td>
              <td class="text-end">
                {{ comp.popularity }}
              </td>
              <td class="text-end d-none d-md-table-cell">
                {{ (comp.relevance ?? 0).toFixed(2) }}
              </td>
              <td class="text-end">
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="openDetail(comp.id)"
                >
                  Открыть
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCompetencesList } from '../js/useCompetences.js'

const router = useRouter()

const search = ref('')
const level = ref('')

const { items, loading, error, fetchCompetences } = useCompetencesList()

const reload = () => {
  const params = {}
  if (search.value) {
    params.search = search.value
  }
  if (level.value) {
    params.level = level.value
  }
  fetchCompetences(params)
}

const openDetail = (id) => {
  router.push({ name: 'CompetenceCoreCompetenceDetail', params: { id } })
}

onMounted(() => {
  reload()
})

watch([search, level], () => {
  // Можно добавить debounce при необходимости
})
</script>


