import { ref, computed } from 'vue'
import { apiClient } from '@/js/api/manager'
import { endpoints } from '@/js/api/endpoints'
import { useToast } from 'vue-toastification'
import { Plus, CircuitBoard, X } from 'lucide-vue-next'

export function useCreateTechnologyForm({ onCreated, categories, technologies }) {
  const toast = useToast()
  const show = ref(false)
  const loading = ref(false)

  const form = ref({
    name: '',
    category: '',
    description: '',
    relevance: 0.5,
    popularity: 0,
    occurrence_count: 0,
    parent_tech: null,
  })

  const errors = ref({
    name: '',
    category: '',
  })

  const categoryOptions = computed(() => categories?.value ?? [])
  const technologiesSource = computed(() => technologies?.value ?? [])

  const nameSuggestions = computed(() => {
    const query = form.value.name.trim().toLowerCase()
    if (!query) return []

    const list = technologiesSource.value
    if (!Array.isArray(list) || !list.length) {
      return []
    }

    const result = []
    for (let i = 0; i < list.length; i += 1) {
      const tech = list[i]
      const name = (tech.name || '').toLowerCase()
      if (name && name.includes(query)) {
        result.push(tech)
        if (result.length >= 5) break
      }
    }

    return result
  })

  const resetForm = () => {
    form.value = {
      name: '',
      category: '',
      description: '',
      relevance: 0.5,
      popularity: 0,
      occurrence_count: 0,
      parent_tech: null,
    }
    errors.value = {
      name: '',
      category: '',
    }
  }

  const open = () => {
    errors.value = { name: '', category: '' }
    show.value = true
  }

  const close = () => {
    if (loading.value) return
    show.value = false
  }

  const validate = () => {
    let ok = true
    errors.value = { name: '', category: '' }

    if (!form.value.name.trim()) {
      errors.value.name = 'Введите название технологии'
      ok = false
    } else if (form.value.name.trim().length < 2) {
      errors.value.name = 'Название должно содержать минимум 2 символа'
      ok = false
    }

    if (!form.value.category) {
      errors.value.category = 'Выберите категорию'
      ok = false
    }

    return ok
  }

  const submit = async () => {
    if (!validate()) return
    loading.value = true

    try {
      const payload = {
        name: form.value.name.trim(),
        category: form.value.category,
        description: form.value.description?.trim() || '',
        relevance: Number(form.value.relevance ?? 0.5),
        popularity: Number(form.value.popularity ?? 0) || 0,
        occurrence_count: Number(form.value.occurrence_count ?? 0) || 0,
        parent_tech: form.value.parent_tech || null,
      }

      const resp = await apiClient.post(endpoints.competenceCore.technologiesList, payload)
      toast.success('Технология успешно создана')

      if (typeof onCreated === 'function') {
        onCreated(resp.data)
      }

      close()
      resetForm()
    } catch (e) {
      // Попробуем прочитать сообщения об ошибке из ответа бэка
      const data = e?.response?.data
      if (data && typeof data === 'object') {
        if (data.name && Array.isArray(data.name) && data.name.length) {
          errors.value.name = data.name[0]
        }
        if (data.category && Array.isArray(data.category) && data.category.length) {
          errors.value.category = data.category[0]
        }
      }
      toast.error('Не удалось создать технологию')
      console.error('Ошибка создания технологии', e)
    } finally {
      loading.value = false
    }
  }

  return {
    // состояние
    show,
    loading,
    form,
    errors,
    categoryOptions,
    nameSuggestions,
    // иконки
    Plus,
    CircuitBoard,
    X,
    // методы
    open,
    close,
    submit,
    resetForm,
  }
}


