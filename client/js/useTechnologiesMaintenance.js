import { ref } from 'vue'
import { apiClient } from '@/js/api/manager'
import { endpoints } from '@/js/api/endpoints'
import { useToast } from 'vue-toastification'

export function useTechnologiesMaintenance({ onChanged } = {}) {
  const toast = useToast()

  const clearing = ref(false)
  const initializing = ref(false)

  const notifyChange = async () => {
    if (typeof onChanged === 'function') {
      await onChanged()
    }
  }

  const clearTechnologies = async () => {
    if (clearing.value) return

    clearing.value = true
    try {
      await apiClient.post(endpoints.competenceCore.technologiesClear)
      toast.success('Все технологии были удалены')
      await notifyChange()
    } catch (e) {
      console.error('Ошибка удаления технологий', e)
      toast.error('Ошибка при удалении технологий')
      throw e
    } finally {
      clearing.value = false
    }
  }

  const initTechnologies = async (options = {}) => {
    if (initializing.value) return

    const payload = {
      clear: options.clear !== undefined ? !!options.clear : true,
      update: options.update !== undefined ? !!options.update : true,
      dry_run: !!options.dry_run,
    }

    initializing.value = true
    try {
      const response = await apiClient.post(
        endpoints.competenceCore.technologiesInit,
        payload,
      )

      if (payload.dry_run) {
        toast.info('Пробный запуск инициализации технологий выполнен')
      } else if (payload.clear) {
        toast.success('Технологии переинициализированы из базового словаря')
      } else {
        toast.success('Инициализация технологий выполнена')
      }

      if (!payload.dry_run) {
        await notifyChange()
      }

      return response.data
    } catch (e) {
      console.error('Ошибка инициализации технологий', e)
      toast.error('Ошибка при инициализации технологий')
      throw e
    } finally {
      initializing.value = false
    }
  }

  return {
    clearing,
    initializing,
    clearTechnologies,
    initTechnologies,
  }
}


