<script setup>
import { ref, watch, computed } from 'vue';
import { XMarkIcon, ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/outline';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  cardType: {
    type: String,
    required: true
  },
  cardTitle: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close']);

// Sorting state
const sortOrder = ref('asc'); // 'asc' for A-Z, 'desc' for Z-A

// Pagination state
const currentPage = ref(1);
const itemsPerPage = 20;

// Reset page when modal opens or items change
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    currentPage.value = 1;
    document.addEventListener('keydown', handleKeydown);
    document.body.style.overflow = 'hidden';
  } else {
    document.removeEventListener('keydown', handleKeydown);
    document.body.style.overflow = '';
  }
});

watch(() => props.items, () => {
  currentPage.value = 1;
});

// Sorted items
const sortedItems = computed(() => {
  if (!props.items || props.items.length === 0) return [];
  
  const sorted = [...props.items].sort((a, b) => {
    const aValue = (a.no_lambung || '').toString().toUpperCase();
    const bValue = (b.no_lambung || '').toString().toUpperCase();
    
    if (sortOrder.value === 'asc') {
      return aValue.localeCompare(bValue, 'id-ID');
    } else {
      return bValue.localeCompare(aValue, 'id-ID');
    }
  });
  
  return sorted;
});

// Computed properties for pagination
const totalPages = computed(() => {
  return Math.ceil((sortedItems.value?.length || 0) / itemsPerPage);
});

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return sortedItems.value?.slice(start, end) || [];
});

const startIndex = computed(() => {
  if (!sortedItems.value || sortedItems.value.length === 0) return 0;
  return (currentPage.value - 1) * itemsPerPage + 1;
});

const endIndex = computed(() => {
  if (!sortedItems.value || sortedItems.value.length === 0) return 0;
  return Math.min(currentPage.value * itemsPerPage, sortedItems.value.length);
});

// Pagination methods
const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const closeModal = () => {
  emit('close');
};

// Toggle sorting order
const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  currentPage.value = 1; // Reset to first page when sorting changes
};

// Get status badge styling
const getStatusBadge = (status) => {
  const badges = {
    'normal': { bg: 'bg-green-100', text: 'text-green-800', label: 'Normal' },
    'abnormal': { bg: 'bg-yellow-100', text: 'text-yellow-800', label: 'Abnormal' },
    'warning': { bg: 'bg-red-100', text: 'text-red-800', label: 'Warning' },
    'pending': { bg: 'bg-gray-100', text: 'text-gray-800', label: 'Pending' },
    'registered': { bg: 'bg-blue-100', text: 'text-blue-800', label: 'Registered' }
  };
  return badges[status] || badges['registered'];
};

// Close on ESC key
const handleKeydown = (e) => {
  if (e.key === 'Escape' && props.isOpen) {
    closeModal();
  }
  // Arrow keys for pagination
  if (e.key === 'ArrowLeft' && props.isOpen) {
    previousPage();
  }
  if (e.key === 'ArrowRight' && props.isOpen) {
    nextPage();
  }
};
</script>

<template>
  <!-- Modal Overlay -->
  <Transition name="modal">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeModal"
    >
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>

      <!-- Modal Container -->
      <div class="flex min-h-screen items-center justify-center p-4">
        <div
          class="relative w-full max-w-4xl bg-white rounded-lg shadow-xl transform transition-all"
          @click.stop
        >
          <!-- Header -->
          <div class="flex items-center justify-between border-b border-gray-200 px-6 py-4">
            <h3 class="text-lg font-semibold text-gray-900">
              {{ cardTitle }}
            </h3>
            <button
              @click="closeModal"
              class="rounded-lg p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
            >
              <XMarkIcon class="h-6 w-6" />
            </button>
          </div>

          <!-- Content -->
          <div class="px-6 py-4 max-h-[60vh] overflow-y-auto">
            <!-- Loading State -->
            <div v-if="loading" class="flex items-center justify-center py-12">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>

            <!-- Empty State -->
            <div v-else-if="!sortedItems || sortedItems.length === 0" class="text-center py-12">
              <p class="text-gray-500 text-sm">Tidak ada data tersedia</p>
            </div>

            <!-- Data Table -->
            <div v-else class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors" @click="toggleSort">
                      <div class="flex items-center gap-2">
                        No. Lambung
                        <span class="text-xs">
                          {{ sortOrder === 'asc' ? '↑ A-Z' : '↓ Z-A' }}
                        </span>
                      </div>
                    </th>
                    <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Plat Nomor
                    </th>
                    <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Tipe
                    </th>
                    <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Merek
                    </th>
                    <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th v-if="sortedItems[0]?.submission_date" scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Tanggal
                    </th>
                    <th v-if="sortedItems[0]?.operator" scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Operator
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(item, index) in paginatedItems" :key="index" class="hover:bg-gray-50 transition-colors">
                    <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                      {{ item.no_lambung || '-' }}
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                      {{ item.plat_nomor || '-' }}
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                      {{ item.vehicle_type || '-' }}
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                      {{ item.merk || '-' }}
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-sm">
                      <span
                        :class="[
                          'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                          getStatusBadge(item.status).bg,
                          getStatusBadge(item.status).text
                        ]"
                      >
                        {{ getStatusBadge(item.status).label }}
                      </span>
                    </td>
                    <td v-if="item.submission_date" class="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                      {{ new Date(item.submission_date).toLocaleDateString('id-ID') }}
                    </td>
                    <td v-if="item.operator" class="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                      {{ item.operator }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Footer with Pagination -->
          <div class="border-t border-gray-200 px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-3">
            <p class="text-sm text-gray-600">
              Menampilkan {{ startIndex }} - {{ endIndex }} dari {{ sortedItems?.length || 0 }} data
            </p>
            
            <!-- Pagination Controls -->
            <div class="flex items-center gap-2">
              <!-- Previous Button -->
              <button
                @click="previousPage"
                :disabled="currentPage === 1"
                class="flex items-center justify-center w-9 h-9 rounded-lg border transition-colors"
                :class="currentPage === 1 
                  ? 'border-gray-200 text-gray-300 cursor-not-allowed' 
                  : 'border-gray-300 text-gray-700 hover:bg-gray-100'"
              >
                <ChevronLeftIcon class="w-5 h-5" />
              </button>
              
              <!-- Page Info -->
              <span class="text-sm text-gray-700 font-medium px-3">
                {{ currentPage }} / {{ totalPages || 1 }}
              </span>
              
              <!-- Next Button -->
              <button
                @click="nextPage"
                :disabled="currentPage >= totalPages"
                class="flex items-center justify-center w-9 h-9 rounded-lg border transition-colors"
                :class="currentPage >= totalPages 
                  ? 'border-gray-200 text-gray-300 cursor-not-allowed' 
                  : 'border-gray-300 text-gray-700 hover:bg-gray-100'"
              >
                <ChevronRightIcon class="w-5 h-5" />
              </button>
            </div>

            <button
              @click="closeModal"
              class="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Tutup
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
}
</style>