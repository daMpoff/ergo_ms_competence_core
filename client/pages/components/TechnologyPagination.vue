<template>
  <div
    v-if="totalPages > 1"
    class="d-flex flex-column flex-md-row justify-content-between align-items-center gap-2 mt-3"
  >
    <div class="text-muted small">
      Страница {{ page }} из {{ totalPages }}
    </div>
    <nav aria-label="Пагинация по технологиям">
      <ul class="pagination pagination-sm mb-0">
        <li class="page-item" :class="{ disabled: page === 1 }">
          <button
            class="page-link"
            type="button"
            @click="page > 1 && $emit('update:page', page - 1)"
          >
            Предыдущая
          </button>
        </li>
        <li
          v-for="p in pageNumbers"
          :key="p"
          class="page-item"
          :class="{ active: p === page, disabled: p === '...' }"
        >
          <button
            class="page-link"
            type="button"
            @click="typeof p === 'number' && $emit('update:page', p)"
          >
            {{ p }}
          </button>
        </li>
        <li class="page-item" :class="{ disabled: page === totalPages }">
          <button
            class="page-link"
            type="button"
            @click="page < totalPages && $emit('update:page', page + 1)"
          >
            Следующая
          </button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
defineProps({
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true },
  pageNumbers: { type: Array, required: true },
})

defineEmits(['update:page'])
</script>

