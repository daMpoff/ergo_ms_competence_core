<template>
  <div class="container py-4">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-3">
      <h2 class="mb-2 mb-md-0">Профили вакансий</h2>
    </div>

    <div class="row g-2 mb-3">
      <div class="col-12 col-md-4">
        <input
          v-model="search"
          type="text"
          class="form-control"
          placeholder="Поиск по названию вакансии"
          @keyup.enter="reload"
        />
      </div>
      <div class="col-12 col-md-3">
        <input
          v-model="source"
          type="text"
          class="form-control"
          placeholder="Источник (HeadHunter, Habr, ...)"
          @keyup.enter="reload"
        />
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
        Профили вакансий не найдены.
      </div>

      <div v-else class="table-responsive">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>Вакансия</th>
              <th class="d-none d-md-table-cell">Источник</th>
              <th class="text-center d-none d-md-table-cell">Компетенций</th>
              <th class="text-end">Создан</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="profile in items" :key="profile.id">
              <td>
                <div class="fw-semibold">
                  {{ profile.vacancy_title }}
                </div>
              </td>
              <td class="d-none d-md-table-cell">
                <span class="badge bg-light text-dark">
                  {{ profile.vacancy_source || '—' }}
                </span>
              </td>
              <td class="text-center d-none d-md-table-cell">
                {{ profile.competences_count ?? '—' }}
              </td>
              <td class="text-end">
                <span class="text-muted small">
                  {{ formatDate(profile.created_at) }}
                </span>
              </td>
              <td class="text-end">
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="openDetail(profile.id)"
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVacancyProfilesList } from '../js/useVacancyProfiles.js'

const router = useRouter()

const search = ref('')
const source = ref('')

const { items, loading, error, fetchProfiles } = useVacancyProfilesList()

const reload = () => {
  const params = {}
  if (search.value) {
    params.search = search.value
  }
  if (source.value) {
    params.vacancy_source = source.value
  }
  fetchProfiles(params)
}

const openDetail = (id) => {
  router.push({ name: 'CompetenceCoreVacancyProfileDetail', params: { id } })
}

const formatDate = (value) => {
  if (!value) return '—'
  try {
    const d = new Date(value)
    return d.toLocaleString('ru-RU')
  } catch {
    return value
  }
}

onMounted(() => {
  reload()
})
</script>


