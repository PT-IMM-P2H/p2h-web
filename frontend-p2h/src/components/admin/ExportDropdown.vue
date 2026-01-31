<template>
  <div class="relative inline-block text-left">
    <button
      @click="toggleDropdown"
      :disabled="disabled || exporting"
      :class="[
        'inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors',
        variant === 'primary'
          ? 'bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300'
          : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 disabled:bg-gray-100',
        'disabled:cursor-not-allowed disabled:opacity-50',
      ]"
    >
      <svg
        v-if="!exporting"
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
      <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
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
      <span>{{ exporting ? "Exporting..." : "Export" }}</span>
      <svg
        class="w-4 h-4 transition-transform"
        :class="{ 'rotate-180': isOpen }"
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

    <!-- Dropdown Menu -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-48 rounded-lg shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50"
    >
      <div class="py-1" role="menu">
        <button
          @click="handleExport('excel')"
          :disabled="exporting"
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          role="menuitem"
        >
          <svg
            class="w-5 h-5 text-green-600"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"
            />
          </svg>
          <span class="font-medium">Excel (.xlsx)</span>
        </button>

        <button
          @click="handleExport('pdf')"
          :disabled="exporting"
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          role="menuitem"
        >
          <svg
            class="w-5 h-5 text-red-600"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20M10.5,11.5C10.5,10.67 11.17,10 12,10C12.83,10 13.5,10.67 13.5,11.5V13.5C13.5,14.33 12.83,15 12,15C11.17,15 10.5,14.33 10.5,13.5V11.5M15,18H9V16H15V18Z"
            />
          </svg>
          <span class="font-medium">PDF (.pdf)</span>
        </button>

        <button
          @click="handleExport('csv')"
          :disabled="exporting"
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          role="menuitem"
        >
          <svg
            class="w-5 h-5 text-blue-600"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20M10,19L12,15L14,19H10M10.5,11A1.5,1.5 0 0,1 9,12.5A1.5,1.5 0 0,1 7.5,11A1.5,1.5 0 0,1 9,9.5A1.5,1.5 0 0,1 10.5,11M16.5,11A1.5,1.5 0 0,1 15,12.5A1.5,1.5 0 0,1 13.5,11A1.5,1.5 0 0,1 15,9.5A1.5,1.5 0 0,1 16.5,11Z"
            />
          </svg>
          <span class="font-medium">CSV (.csv)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import apiService from "@/services/api";

const props = defineProps({
  exportEndpoint: {
    type: String,
    required: true,
  },
  filters: {
    type: Object,
    default: () => ({}),
  },
  variant: {
    type: String,
    default: "primary", // primary or secondary
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["export-start", "export-complete", "export-error"]);

const isOpen = ref(false);
const exporting = ref(false);

const toggleDropdown = () => {
  if (!exporting.value && !props.disabled) {
    isOpen.value = !isOpen.value;
  }
};

const closeDropdown = () => {
  isOpen.value = false;
};

const handleClickOutside = (event) => {
  if (!event.target.closest(".relative")) {
    closeDropdown();
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});

const handleExport = async (format) => {
  closeDropdown();
  exporting.value = true;
  emit("export-start", format);

  try {
    // Build query parameters - only add defined values
    const params = new URLSearchParams();
    params.append("format", format);

    // Add filters only if they have valid values
    for (const [key, value] of Object.entries(props.filters)) {
      if (
        value !== undefined &&
        value !== null &&
        value !== "" &&
        value !== "undefined"
      ) {
        params.append(key, value);
      }
    }

    // Use apiService.instance to automatically handle Authorization headers
    const response = await apiService.instance.get(
      `${props.exportEndpoint}?${params.toString()}`,
      {
        responseType: "blob",
      },
    );

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;

    // Extract filename from Content-Disposition header
    const contentDisposition = response.headers["content-disposition"];
    const extensionMap = { excel: "xlsx", pdf: "pdf", csv: "csv" };
    let filename = `export_${Date.now()}.${extensionMap[format] || format}`;
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i);
      if (filenameMatch) {
        filename = filenameMatch[1].replace(/"/g, "");
      }
    }

    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);

    emit("export-complete", { format, filename });
  } catch (error) {
    console.error("Export error:", error);
    const errorMessage =
      error.response?.data?.message || error.message || "Gagal mengekspor data";
    alert("Gagal mengekspor data: " + errorMessage);
    emit("export-error", { format, error: errorMessage });
  } finally {
    exporting.value = false;
  }
};
</script>
