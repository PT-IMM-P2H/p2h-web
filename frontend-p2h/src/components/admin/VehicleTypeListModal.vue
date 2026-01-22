<template>
  <!-- Modal Overlay -->
  <Transition name="modal">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      @click.self="$emit('close')"
    >
      <!-- Modal Container -->
      <div
        class="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] flex flex-col"
        @click.stop
      >
        <!-- Header -->
        <div
          class="flex items-center justify-between p-6 border-b border-gray-200"
        >
          <div>
            <h3 class="text-xl font-semibold text-gray-900">
              Kelola Tipe Kendaraan
            </h3>
            <p class="text-sm text-gray-500 mt-1">
              Manage semua tipe kendaraan yang tersedia dalam sistem
            </p>
          </div>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- Body -->
        <div class="flex-1 overflow-y-auto p-6">
          <!-- Action Bar -->
          <div class="flex items-center justify-between mb-4">
            <button
              @click="openAddModal"
              class="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
            >
              <PlusIcon class="w-5 h-5" />
              <span>Tambah Tipe Baru</span>
            </button>

            <!-- Search -->
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Cari tipe kendaraan..."
              class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent w-64"
            />
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="flex items-center justify-center py-12">
            <div class="text-center">
              <svg
                class="animate-spin h-10 w-10 text-purple-600 mx-auto mb-4"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              <p class="text-gray-600">Loading...</p>
            </div>
          </div>

          <!-- Empty State -->
          <div
            v-else-if="filteredVehicleTypes.length === 0"
            class="flex flex-col items-center justify-center py-12 text-gray-500"
          >
            <TruckIcon class="w-16 h-16 mb-4 text-gray-300" />
            <p class="text-lg font-medium">Tidak ada tipe kendaraan</p>
            <p class="text-sm mt-1">
              {{
                searchQuery
                  ? "Tidak ditemukan hasil pencarian"
                  : "Klik tombol di atas untuk menambah tipe kendaraan baru"
              }}
            </p>
          </div>

          <!-- Table -->
          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Nama Tipe
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Deskripsi
                  </th>
                  <th
                    class="px-4 py-3 text-center text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Status
                  </th>
                  <th
                    class="px-4 py-3 text-center text-xs font-medium text-gray-600 uppercase tracking-wider w-32"
                  >
                    Aksi
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="type in filteredVehicleTypes"
                  :key="type.id"
                  class="hover:bg-gray-50 transition"
                >
                  <td class="px-4 py-3 text-sm font-medium text-gray-900">
                    {{ type.name }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-600">
                    {{ type.description || "-" }}
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span
                      :class="[
                        'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                        type.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800',
                      ]"
                    >
                      {{ type.is_active ? "Aktif" : "Nonaktif" }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center">
                    <div class="flex items-center justify-center gap-2">
                      <button
                        @click="openEditModal(type)"
                        class="p-1.5 text-blue-600 hover:bg-blue-50 rounded transition"
                        title="Edit"
                      >
                        <PencilIcon class="w-4 h-4" />
                      </button>
                      <button
                        @click="confirmDeleteVehicleType(type)"
                        class="p-1.5 text-red-600 hover:bg-red-50 rounded transition"
                        title="Hapus"
                      >
                        <TrashIcon class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Footer -->
        <div
          class="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50"
        >
          <p class="text-sm text-gray-600">
            Total: <span class="font-semibold">{{ vehicleTypes.length }}</span>
            tipe kendaraan
          </p>
          <button
            @click="$emit('close')"
            class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from "vue";
import {
  XMarkIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  TruckIcon,
} from "@heroicons/vue/24/outline";

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  vehicleTypes: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits([
  "close",
  "add",
  "edit",
  "delete",
  "refresh",
]);

const searchQuery = ref("");

const filteredVehicleTypes = computed(() => {
  if (!searchQuery.value) return props.vehicleTypes;

  const query = searchQuery.value.toLowerCase();
  return props.vehicleTypes.filter(
    (type) =>
      type.name.toLowerCase().includes(query) ||
      (type.description && type.description.toLowerCase().includes(query))
  );
});

const openAddModal = () => {
  emit("add");
};

const openEditModal = (vehicleType) => {
  emit("edit", vehicleType);
};

const confirmDeleteVehicleType = (vehicleType) => {
  emit("delete", vehicleType);
};
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: transform 0.3s ease;
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  transform: scale(0.9);
}
</style>
