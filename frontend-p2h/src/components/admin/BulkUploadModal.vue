<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
  >
    <div
      class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
    >
      <!-- Header -->
      <div
        class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 rounded-t-lg"
      >
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-semibold text-gray-900">{{ title }}</h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition-colors"
            :disabled="uploading"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Body -->
      <div class="px-6 py-4">
        <!-- Instructions -->
        <div class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 class="font-semibold text-blue-900 mb-2">📋 Instruksi Upload</h4>
          <ul class="text-sm text-blue-800 space-y-1 list-disc list-inside">
            <li>Download template terlebih dahulu</li>
            <li>Isi data sesuai format yang tersedia</li>
            <li>Upload file Excel (.xlsx atau .xls)</li>
            <li>Data yang error akan dilewati dan dilaporkan</li>
          </ul>
        </div>

        <!-- Download Template Button -->
        <div class="mb-6">
          <button
            @click="downloadTemplate"
            class="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            :disabled="uploading"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Download Template
          </button>
        </div>

        <!-- File Upload Area -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Upload File Excel
          </label>
          <div
            @dragover.prevent="dragOver = true"
            @dragleave.prevent="dragOver = false"
            @drop.prevent="handleDrop"
            :class="[
              'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
              dragOver
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 bg-gray-50',
              uploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
            ]"
            @click="$refs.fileInput.click()"
          >
            <input
              ref="fileInput"
              type="file"
              accept=".xlsx,.xls"
              @change="handleFileSelect"
              class="hidden"
              :disabled="uploading"
            />

            <svg
              v-if="!selectedFile"
              class="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>

            <div
              v-if="selectedFile"
              class="flex items-center justify-center gap-3"
            >
              <svg
                class="h-10 w-10 text-green-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <div class="text-left">
                <p class="text-sm font-medium text-gray-900">
                  {{ selectedFile.name }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ formatFileSize(selectedFile.size) }}
                </p>
              </div>
            </div>

            <p v-if="!selectedFile" class="mt-2 text-sm text-gray-600">
              Klik atau drag & drop file Excel di sini
            </p>
            <p v-if="!selectedFile" class="text-xs text-gray-500 mt-1">
              Format: .xlsx atau .xls (Maks. 10MB)
            </p>
          </div>
        </div>

        <!-- Upload Progress -->
        <div v-if="uploading" class="mb-6">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700">Mengupload...</span>
            <span class="text-sm text-gray-500">{{ uploadProgress }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-blue-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: uploadProgress + '%' }"
            ></div>
          </div>
        </div>

        <!-- Upload Result -->
        <div v-if="uploadResult" class="mb-6">
          <div
            :class="[
              'p-4 rounded-lg border',
              uploadResult.error_count === 0
                ? 'bg-green-50 border-green-200'
                : 'bg-yellow-50 border-yellow-200',
            ]"
          >
            <div class="flex items-start gap-3">
              <svg
                v-if="uploadResult.error_count === 0"
                class="h-6 w-6 text-green-500 shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <svg
                v-else
                class="h-6 w-6 text-yellow-500 shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
              <div class="flex-1">
                <h4
                  :class="[
                    'font-semibold mb-2',
                    uploadResult.error_count === 0
                      ? 'text-green-900'
                      : 'text-yellow-900',
                  ]"
                >
                  Import Selesai
                </h4>
                <div class="text-sm space-y-1">
                  <p
                    :class="
                      uploadResult.error_count === 0
                        ? 'text-green-800'
                        : 'text-yellow-800'
                    "
                  >
                    ✅ Berhasil:
                    <strong>{{ uploadResult.success_count }}</strong> dari
                    {{ uploadResult.total_rows }} baris
                  </p>
                  <p
                    v-if="uploadResult.error_count > 0"
                    class="text-yellow-800"
                  >
                    ⚠️ Error:
                    <strong>{{ uploadResult.error_count }}</strong> baris
                    dilewati
                  </p>
                </div>

                <!-- Error Details -->
                <div
                  v-if="uploadResult.errors && uploadResult.errors.length > 0"
                  class="mt-3"
                >
                  <button
                    @click="showErrors = !showErrors"
                    class="text-sm font-medium text-yellow-700 hover:text-yellow-800 flex items-center gap-1"
                  >
                    {{ showErrors ? "Sembunyikan" : "Lihat" }} Detail Error
                    <svg
                      class="w-4 h-4 transition-transform"
                      :class="{ 'rotate-180': showErrors }"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>

                  <div v-if="showErrors" class="mt-2 max-h-48 overflow-y-auto">
                    <div
                      class="bg-white rounded border border-yellow-300 divide-y divide-yellow-200"
                    >
                      <div
                        v-for="(error, idx) in uploadResult.errors.slice(0, 20)"
                        :key="idx"
                        class="px-3 py-2 text-xs"
                      >
                        <span class="font-semibold text-gray-900"
                          >Baris {{ error.row }}:</span
                        >
                        <span class="text-gray-700 ml-1">{{
                          error.message
                        }}</span>
                        <span v-if="error.field" class="text-gray-500 ml-1"
                          >(Field: {{ error.field }})</span
                        >
                      </div>
                      <div
                        v-if="uploadResult.errors.length > 20"
                        class="px-3 py-2 text-xs text-gray-600 italic"
                      >
                        ... dan {{ uploadResult.errors.length - 20 }} error
                        lainnya
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div
        class="sticky bottom-0 bg-gray-50 px-6 py-4 border-t border-gray-200 rounded-b-lg flex justify-end gap-3"
      >
        <button
          @click="$emit('close')"
          class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          :disabled="uploading"
        >
          {{ uploadResult ? "Tutup" : "Batal" }}
        </button>
        <button
          v-if="selectedFile && !uploadResult"
          @click="handleUpload"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="uploading || !selectedFile"
        >
          <span v-if="!uploading">Upload Data</span>
          <span v-else>Mengupload...</span>
        </button>
        <button
          v-if="uploadResult"
          @click="reset"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Upload Lagi
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import apiService from "@/services/api";
import { STORAGE_KEYS } from "@/constants";

const props = defineProps({
  isOpen: Boolean,
  title: String,
  uploadEndpoint: String, // Kept for backward compat, but logic now uses apiService
  templateEndpoint: String, // Kept for backward compat
  uploadType: {
    type: String,
    default: "vehicles", // 'vehicles' or 'users'
    validator: (value) => ["vehicles", "users"].includes(value),
  },
});

const emit = defineEmits(["close", "success"]);

const selectedFile = ref(null);
const uploading = ref(false);
const uploadProgress = ref(0);
const uploadResult = ref(null);
const dragOver = ref(false);
const showErrors = ref(false);
const fileInput = ref(null);

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      reset();
    }
  },
);

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    validateAndSetFile(file);
  }
};

const handleDrop = (event) => {
  dragOver.value = false;
  const file = event.dataTransfer.files[0];
  if (file) {
    validateAndSetFile(file);
  }
};

const validateAndSetFile = (file) => {
  // Validate file type
  const validTypes = [
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
  ];
  if (!validTypes.includes(file.type) && !file.name.match(/\.(xlsx|xls)$/i)) {
    alert("File harus berformat Excel (.xlsx atau .xls)");
    return;
  }

  // Validate file size (10MB)
  if (file.size > 10 * 1024 * 1024) {
    alert("Ukuran file maksimal 10MB");
    return;
  }

  selectedFile.value = file;
  uploadResult.value = null;
};

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + " KB";
  return (bytes / (1024 * 1024)).toFixed(2) + " MB";
};

const downloadTemplate = () => {
  // Determine template type from uploadType prop
  const templateType = props.uploadType === "users" ? "users" : "vehicles";
  const baseUrl = import.meta.env.VITE_API_BASE_URL;
  
  // Get auth token from localStorage
  const token = localStorage.getItem('STORAGE_KEYS.AUTH_TOKEN');
    
  // Debug: Check all localStorage keys
  console.log('🔍 Download Template Debug:', {
    storageKey: STORAGE_KEYS.AUTH_TOKEN,
    tokenExists: !!token,
    tokenLength: token?.length,
    allKeys: Object.keys(localStorage),
    allTokens: {
      auth_token: localStorage.getItem('auth_token'),
      token: localStorage.getItem('token'),
      access_token: localStorage.getItem('access_token')
    }
  });
  
  if (!token) {
    alert('Sesi login tidak ditemukan. Silahkan login kembali.');
    return;
  }
  
  // Create download link with auth header via fetch
  const url = `${baseUrl}/bulk-upload/templates/${templateType}`;
  
  fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Gagal mendownload template');
    }
    return response.blob();
  })
  .then(blob => {
    // Create download link
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = templateType === 'users' 
      ? 'template_data_pengguna.xlsx' 
      : 'template_data_kendaraan.xlsx';
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(downloadUrl);
  })
  .catch(error => {
    console.error('Error downloading template:', error);
    alert('Gagal mendownload template. Pastikan Anda memiliki akses admin.');
  });
};

const handleUpload = async () => {
  if (!selectedFile.value) return;

  uploading.value = true;
  uploadProgress.value = 0;
  uploadResult.value = null;

  try {
    const formData = new FormData();
    formData.append("file", selectedFile.value);

    // Determine upload method
    let uploadMethod;
    if (props.uploadType === "users") {
      uploadMethod = apiService.bulkUpload.uploadUsers;
    } else {
      uploadMethod = apiService.bulkUpload.uploadVehicles;
    }

    const response = await uploadMethod(formData, (progressEvent) => {
      uploadProgress.value = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total,
      );
    });

    if (response.data.payload) {
      uploadResult.value = response.data.payload;
      if (uploadResult.value.success_count > 0) {
        emit("success");
      }
    }
  } catch (error) {
    console.error("Upload error:", error);
    alert(
      "Gagal mengupload file: " +
        (error.response?.data?.message || error.message),
    );
  } finally {
    uploading.value = false;
  }
};

const reset = () => {
  selectedFile.value = null;
  uploading.value = false;
  uploadProgress.value = 0;
  uploadResult.value = null;
  showErrors.value = false;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};
</script>
