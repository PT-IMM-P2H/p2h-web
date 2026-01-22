<script setup>
import { computed, defineProps } from 'vue'

const props = defineProps({
  columns: {
    type: Array,
    required: true,
    // Example: [{ key: 'name', label: 'Nama', hideOnMobile: false, class: 'min-w-32' }]
  },
  data: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  emptyText: {
    type: String,
    default: 'Tidak ada data'
  }
})

const visibleColumns = computed(() => {
  return props.columns.filter(col => !col.hideOnMobile || window.innerWidth >= 768)
})
</script>

<template>
  <div class="overflow-x-auto -mx-3 md:mx-0 md:rounded-lg border-b md:border">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-8 md:py-12 bg-white">
      <div class="animate-spin rounded-full h-10 w-10 md:h-12 md:w-12 border-b-2 border-indigo-500"></div>
      <span class="ml-3 text-gray-600 text-sm md:text-base">Memuat data...</span>
    </div>

    <!-- Empty State -->
    <div v-else-if="!data || data.length === 0" class="flex justify-center items-center py-8 md:py-12 bg-white">
      <p class="text-gray-500 text-sm md:text-base">{{ emptyText }}</p>
    </div>

    <!-- Table -->
    <table v-else class="w-full border-collapse bg-white text-sm md:text-base">
      <thead>
        <tr class="border-b-2 border-gray-400 bg-gray-50">
          <th
            v-for="column in columns"
            :key="column.key"
            :class="[
              'px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm',
              column.hideOnMobile ? 'hidden md:table-cell' : '',
              column.headerClass || ''
            ]"
          >
            {{ column.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <slot name="body" :data="data">
          <tr
            v-for="(row, index) in data"
            :key="index"
            class="border-b border-gray-200 hover:bg-gray-50 transition-colors"
          >
            <td
              v-for="column in columns"
              :key="column.key"
              :class="[
                'px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm',
                column.hideOnMobile ? 'hidden md:table-cell' : '',
                column.cellClass || ''
              ]"
            >
              <slot :name="`cell-${column.key}`" :row="row" :value="row[column.key]">
                {{ row[column.key] }}
              </slot>
            </td>
          </tr>
        </slot>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
/* Ensure table is scrollable on mobile */
@media (max-width: 767px) {
  table {
    min-width: 600px;
  }
}
</style>
