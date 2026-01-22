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
        class="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col"
        @click.stop
      >
        <!-- Header -->
        <div
          class="flex items-center justify-between p-6 border-b border-gray-200"
        >
          <h3 class="text-xl font-semibold text-gray-900">
            {{ editMode ? "Edit Tipe Kendaraan" : "Tambah Tipe Kendaraan" }}
          </h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- Body -->
        <div class="flex-1 overflow-y-auto p-6">
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <!-- Nama Tipe Kendaraan -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Nama Tipe Kendaraan <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.name"
                type="text"
                placeholder="Contoh: Light Vehicle, Bus, dll"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-gray-900 placeholder-gray-400"
                required
              />
            </div>

            <!-- Deskripsi (Optional) -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Deskripsi (Opsional)
              </label>
              <textarea
                v-model="form.description"
                rows="3"
                placeholder="Deskripsi singkat tentang tipe kendaraan ini..."
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none text-gray-900 placeholder-gray-400"
              ></textarea>
            </div>

            <!-- Status Aktif -->
            <div class="flex items-center gap-3">
              <input
                v-model="form.is_active"
                type="checkbox"
                id="is_active"
                class="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
              />
              <label for="is_active" class="text-sm font-medium text-gray-700">
                Aktif (dapat dipilih saat membuat kendaraan baru)
              </label>
            </div>
          </form>
        </div>

        <!-- Footer -->
        <div
          class="flex items-center justify-end gap-3 p-6 border-t border-gray-200"
        >
          <button
            @click="$emit('close')"
            class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
          >
            Batal
          </button>
          <button
            @click="handleSubmit"
            :disabled="loading || !form.name.trim()"
            class="px-4 py-2 text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <span v-if="loading">
              <svg
                class="animate-spin h-5 w-5 text-white"
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
            </span>
            <span v-else>{{ editMode ? "Update" : "Simpan" }}</span>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from "vue";
import { XMarkIcon } from "@heroicons/vue/24/outline";

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  editMode: {
    type: Boolean,
    default: false,
  },
  vehicleType: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "submit"]);

const form = ref({
  name: "",
  description: "",
  is_active: true,
});

// Watch for changes in vehicleType prop (for edit mode)
watch(
  () => props.vehicleType,
  (newVal) => {
    if (newVal && props.editMode) {
      form.value = {
        name: newVal.name || "",
        description: newVal.description || "",
        is_active: newVal.is_active !== undefined ? newVal.is_active : true,
      };
    } else if (!props.editMode) {
      // Reset form when not in edit mode
      form.value = {
        name: "",
        description: "",
        is_active: true,
      };
    }
  },
  { immediate: true }
);

// Reset form when modal closes
watch(
  () => props.isOpen,
  (newVal) => {
    if (!newVal) {
      form.value = {
        name: "",
        description: "",
        is_active: true,
      };
    }
  }
);

const handleSubmit = () => {
  if (form.value.name.trim()) {
    emit("submit", { ...form.value });
  }
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
