<template>
  <div
    class="modal fade show d-block tech-create-modal-backdrop"
    tabindex="-1"
    role="dialog"
    aria-modal="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
      <div class="modal-content tech-create-modal">
        <div class="modal-header">
          <h5 class="modal-title d-flex align-items-center gap-2">
            <CircuitBoard :size="20" :stroke-width="1.9" />
            <span>Новая технология</span>
          </h5>
          <button
            type="button"
            class="btn-close"
            aria-label="Закрыть"
            @click="close"
          >
            <X :size="16" :stroke-width="1.9" />
          </button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="submit">
            <div class="tech-section">
              <div class="tech-section-header">
                <div class="tech-section-title">Основная информация</div>
                <div class="tech-section-subtitle">
                  Название, категория и базовые параметры технологии
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Название технологии</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.name }"
                  placeholder="Например: React, PostgreSQL, Kubernetes"
                  autocomplete="off"
                />
                <div v-if="errors.name" class="invalid-feedback">
                  {{ errors.name }}
                </div>

                <div v-if="exactMatch" class="tech-existing-warning mt-1">
                  <span class="tech-existing-warning-title">Технология с таким названием уже существует:</span>
                  <span class="tech-existing-warning-name">
                    «{{ exactMatch.name }}»
                    <span v-if="exactMatch.category_display" class="text-muted">
                      ({{ exactMatch.category_display }})
                    </span>
                  </span>
                </div>

                <div v-else-if="suggestions.length" class="tech-existing-suggestions mt-1">
                  <span class="tech-existing-suggestions-title">Похожие существующие технологии:</span>
                  <div class="tech-existing-suggestions-list">
                    <span
                      v-for="item in suggestions"
                      :key="item.id"
                      class="badge rounded-pill bg-light text-body tech-existing-suggestion-badge"
                    >
                      <span class="tech-existing-suggestion-name">{{ item.name }}</span>
                      <span v-if="item.category_display" class="tech-existing-suggestion-category">
                        • {{ item.category_display }}
                      </span>
                    </span>
                  </div>
                </div>
              </div>

              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Категория</label>
                  <select
                    v-model="form.category"
                    class="form-select"
                    :class="{ 'is-invalid': errors.category }"
                  >
                    <option value="">Выберите категорию</option>
                    <option
                      v-for="cat in categoryOptions"
                      :key="cat.value"
                      :value="cat.value"
                    >
                      {{ cat.label }}
                    </option>
                  </select>
                  <div v-if="errors.category" class="invalid-feedback">
                    {{ errors.category }}
                  </div>
                </div>

                <div class="col-md-6">
                  <label class="form-label d-flex justify-content-between">
                    <span>Релевантность</span>
                    <span class="text-muted small">
                      {{ Number(form.relevance).toFixed(2) }}
                    </span>
                  </label>
                  <input
                    v-model.number="form.relevance"
                    type="range"
                    min="0"
                    max="1"
                    step="0.01"
                    class="form-range"
                  />
                </div>
              </div>
            </div>

            <div class="tech-section mt-3">
              <div class="tech-section-header">
                <div class="tech-section-title">Метрики и связи</div>
                <div class="tech-section-subtitle">
                  Необязательные параметры, которые можно заполнить позже
                </div>
              </div>

              <div class="row g-3 mt-1">
                <div class="col-md-4">
                  <label class="form-label">Популярность</label>
                  <input
                    v-model.number="form.popularity"
                    type="number"
                    min="0"
                    class="form-control"
                    placeholder="0"
                  />
                </div>
                <div class="col-md-4">
                  <label class="form-label">Упоминания</label>
                  <input
                    v-model.number="form.occurrence_count"
                    type="number"
                    min="0"
                    class="form-control"
                    placeholder="0"
                  />
                </div>
                <div class="col-md-4">
                  <label class="form-label">Родительская технология (ID)</label>
                  <input
                    v-model.number="form.parent_tech"
                    type="number"
                    min="1"
                    class="form-control"
                    placeholder="Не задано"
                  />
                </div>
              </div>
            </div>

            <div class="tech-section mt-3">
              <div class="tech-section-header mb-2">
                <div class="tech-section-title">Описание</div>
                <div class="tech-section-subtitle">
                  Кратко опишите назначение, область применения и важные детали
                </div>
              </div>

              <textarea
                v-model="form.description"
                rows="3"
                class="form-control"
                placeholder="Например: JavaScript‑библиотека для построения пользовательских интерфейсов..."
              />
            </div>
          </form>
        </div>

        <div class="modal-footer justify-content-between">
          <div class="text-muted small">
            Поля «Популярность», «Упоминания» и «Родительская технология» можно заполнить позже.
          </div>
          <div class="d-flex gap-2">
            <button
              type="button"
              class="btn btn-outline-secondary"
              :disabled="loading"
              @click="close"
            >
              Отмена
            </button>
            <button
              type="button"
              class="btn btn-primary d-flex align-items-center gap-2"
              :disabled="loading"
              @click="submit"
            >
              <span class="d-flex align-items-center justify-content-center">
                <Plus :size="16" :stroke-width="2.1" />
              </span>
              <span>{{ loading ? 'Создание...' : 'Создать технологию' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, toRef, watch } from 'vue'
import { useCreateTechnologyForm } from '../js/useCreateTechnologyForm.js'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  categories: {
    type: Array,
    default: () => [],
  },
  existingTechnologies: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue', 'created'])

const categoriesRef = toRef(props, 'categories')

const { show, loading, form, errors, categoryOptions, Plus, CircuitBoard, X, open, close, submit } =
  useCreateTechnologyForm({
    onCreated: (item) => {
      emit('created', item)
    },
    categories: categoriesRef,
  })

const suggestions = computed(() => {
  const term = form.value.name?.trim().toLowerCase()
  if (!term || term.length < 2) {
    return []
  }

  const list = props.existingTechnologies || []
  const matches = list.filter((tech) => {
    if (!tech.name) return false
    return tech.name.toLowerCase().includes(term)
  })

  return matches.slice(0, 5)
})

const exactMatch = computed(() => {
  const term = form.value.name?.trim().toLowerCase()
  if (!term) return null

  const list = props.existingTechnologies || []
  return list.find((tech) => tech.name && tech.name.toLowerCase() === term) || null
})

if (props.modelValue) {
  open()
}

watch(
  () => props.modelValue,
  (value) => {
    if (value) {
      open()
    } else {
      close()
    }
  },
)

watch(
  show,
  (value) => {
    if (value !== props.modelValue) {
      emit('update:modelValue', value)
    }
  },
)
</script>

<style scoped src="../scss/TechnologyCreateModal.scss"></style>


