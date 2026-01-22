<script setup>
import { ref, watch } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/outline';
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

const closeModal = () => {
  emit('close');
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
};

watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    document.addEventListener('keydown', handleKeydown);
    document.body.style.overflow = 'hidden';
  } else {
    document.removeEventListener('keydown', handleKeydown);
    document.body.style.overflow = '';
  }
});
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
            <div v-else-if="!items || items.length === 0" class="text-center py-12">
              <p class="text-gray-500 text-sm">Tidak ada data tersedia</p>
            </div>

            <!-- Data Table -->
            <div v-else class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      No. Lambung
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
                    <th v-if="items[0]?.submission_date" scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Tanggal
                    </th>
                    <th v-if="items[0]?.operator" scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Operator
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(item, index) in items" :key="index" class="hover:bg-gray-50 transition-colors">
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

          <!-- Footer -->
          <div class="border-t border-gray-200 px-6 py-4 flex justify-between items-center">
            <p class="text-sm text-gray-600">
              Menampilkan {{ items?.length || 0 }} data
            </p>
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
