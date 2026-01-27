<script setup>
import { ref, computed, onMounted } from "vue";
import Aside from "../../bar/aside.vue";
import HeaderAdmin from "../../bar/header_admin.vue";
import {
  MagnifyingGlassIcon,
  TrashIcon,
  PlusIcon,
  XMarkIcon,
  PencilSquareIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  CheckIcon,
} from "@heroicons/vue/24/outline";
import { PencilIcon } from "@heroicons/vue/24/solid";
import apiService from "@/services/api";
import { useSidebarProvider } from "../../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();

const selectedRowIds = ref([]);
const selectAllChecked = ref(false);
const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = ref(10);
const showTambahPerusahaan = ref(false);
const sortOrder = ref("asc");
const isLoading = ref(false);
const errorMessage = ref("");

// Form data untuk tambah/edit
const formData = ref({
  nama_perusahaan: "",
  status: "",
});

const editingId = ref(null);

const openTambahPerusahaan = () => {
  formData.value = {
    nama_perusahaan: "",
    status: "",
  };
  editingId.value = null;
  showTambahPerusahaan.value = true;
};

const closeTambahPerusahaan = () => {
  showTambahPerusahaan.value = false;
  formData.value = {
    nama_perusahaan: "",
    status: "",
  };
  errorMessage.value = "";
};

const showEditPerusahaan = ref(false);

const openEditPerusahaan = (company) => {
  formData.value = {
    nama_perusahaan: company.nama_perusahaan,
    status: company.status || "",
  };
  editingId.value = company.id;
  showEditPerusahaan.value = true;
};

const closeEditPerusahaan = () => {
  showEditPerusahaan.value = false;
  formData.value = {
    nama_perusahaan: "",
    status: "",
  };
  editingId.value = null;
  errorMessage.value = "";
};

const tableData = ref([]);

// Fetch data dari backend
const fetchCompanies = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const response = await apiService.master.getCompanies();

    if (response.data.status === "success" || response.data.success) {
      tableData.value = response.data.payload.map((company) => ({
        id: company.id,
        namaPerusahaan: company.nama_perusahaan,
        status: company.status || "-",
      }));
    } else {
      errorMessage.value = response.data.message || "Gagal mengambil data";
    }
  } catch (error) {
    console.error("Error fetching companies:", error);

    const errorMsg =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Gagal mengambil data perusahaan";

    errorMessage.value = errorMsg;
  } finally {
    isLoading.value = false;
  }
};

// Tambah perusahaan baru
const handleTambahPerusahaan = async () => {
  if (!formData.value.nama_perusahaan.trim()) {
    errorMessage.value = "Nama perusahaan wajib diisi";
    alert("Nama perusahaan wajib diisi!");
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";

  try {
    const payload = {
      nama_perusahaan: formData.value.nama_perusahaan,
      status: formData.value.status || null,
    };

    const response = await apiService.master.createCompany(payload);

    if (response.data.status === "success" || response.data.success) {
      alert("Perusahaan berhasil ditambahkan");
      closeTambahPerusahaan();
      await fetchCompanies();
    } else {
      errorMessage.value =
        response.data.message || "Gagal menambahkan perusahaan";
    }
  } catch (error) {
    console.error("Error creating company:", error);

    const errorMsg =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Gagal menambahkan perusahaan";

    errorMessage.value = errorMsg;
    alert(`Error: ${errorMsg}`);
  } finally {
    isLoading.value = false;
  }
};

// Update perusahaan
const handleEditPerusahaan = async () => {
  if (!formData.value.nama_perusahaan.trim()) {
    errorMessage.value = "Nama perusahaan wajib diisi";
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";
  try {
    const response = await apiService.master.updateCompany(editingId.value, {
      nama_perusahaan: formData.value.nama_perusahaan,
      status: formData.value.status || null,
    });

    if (response.data.status === "success" || response.data.success) {
      await fetchCompanies();
      closeEditPerusahaan();
      alert("Perusahaan berhasil diupdate");
    }
  } catch (error) {
    console.error("Error updating company:", error);
    errorMessage.value =
      error.response?.data?.detail || "Gagal mengupdate perusahaan";
  } finally {
    isLoading.value = false;
  }
};

// Hapus perusahaan (soft delete)
const handleDeleteCompanies = async () => {
  if (selectedRowIds.value.length === 0) {
    alert("Pilih perusahaan yang ingin dihapus!");
    return;
  }

  if (
    !confirm(`Yakin ingin menghapus ${selectedRowIds.value.length} perusahaan?`)
  ) {
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";
  let deletedCount = 0;

  try {
    // Hapus satu per satu
    for (const id of selectedRowIds.value) {
      await apiService.master.deleteCompany(id);
      deletedCount++;
    }

    // Reset selection
    selectedRowIds.value = [];
    selectAllChecked.value = false;

    // Clear current data to force refresh
    tableData.value = [];

    // Refresh data from backend
    await fetchCompanies();

    alert(`${deletedCount} perusahaan berhasil dihapus`);
  } catch (error) {
    console.error("Error deleting companies:", error);

    const errorMsg =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Gagal menghapus perusahaan";

    errorMessage.value = errorMsg;
    alert(
      `Error: ${errorMsg}\n\nBerhasil dihapus: ${deletedCount} dari ${selectedRowIds.value.length}`,
    );
  } finally {
    isLoading.value = false;
  }
};

// Load data saat component di-mount
onMounted(() => {
  fetchCompanies();
});

const selectRow = (rowId) => {
  const index = selectedRowIds.value.indexOf(rowId);
  if (index > -1) {
    // Hapus ID jika sudah ada
    selectedRowIds.value.splice(index, 1);
  } else {
    // Tambah ID jika belum ada
    selectedRowIds.value.push(rowId);
  }
  // Update selectAllChecked
  selectAllChecked.value =
    selectedRowIds.value.length === tableData.value.length;
};

const toggleSelectAll = () => {
  selectAllChecked.value = !selectAllChecked.value;
  if (selectAllChecked.value) {
    // Pilih semua
    selectedRowIds.value = tableData.value.map((row) => row.id);
  } else {
    // Kosongkan semua
    selectedRowIds.value = [];
  }
};

const isRowSelected = (rowId) => {
  return selectedRowIds.value.includes(rowId);
};

// Helper function untuk normalize string (hapus whitespace dan karakter khusus)
const normalizeString = (str) => {
  return str.toLowerCase().replace(/[\s\-./]/g, "");
};

// Filter data berdasarkan search query
const filteredTableData = computed(() => {
  if (!searchQuery.value.trim()) {
    return tableData.value;
  }

  const query = normalizeString(searchQuery.value);
  return tableData.value.filter((row) => {
    return normalizeString(row.namaPerusahaan).includes(query);
  });
});

// Pagination computed
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredTableData.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredTableData.value.length / itemsPerPage.value);
});

const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage.value + 1;
});

const endIndex = computed(() => {
  return Math.min(
    currentPage.value * itemsPerPage.value,
    filteredTableData.value.length,
  );
});

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const sortByCompanyName = () => {
  if (sortOrder.value === "asc") {
    sortOrder.value = "desc";
    tableData.value = [...tableData.value].sort((a, b) =>
      b.namaPerusahaan.localeCompare(a.namaPerusahaan),
    );
  } else {
    sortOrder.value = "asc";
    tableData.value = [...tableData.value].sort((a, b) =>
      a.namaPerusahaan.localeCompare(b.namaPerusahaan),
    );
  }
  currentPage.value = 1;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};
</script>

<template>
  <div class="h-screen flex flex-col font-['Montserrat']">
    <div class="flex flex-1 overflow-hidden">
      <!-- Aside Sidebar - Push content style -->
      <Aside :isOpen="isSidebarOpen" :onClose="closeSidebar" />

      <!-- Main Content Area -->
      <div class="flex flex-col flex-1 min-w-0 overflow-hidden">
        <HeaderAdmin />

        <!-- Content -->
        <main
          class="bg-[#EFEFEF] flex-1 overflow-y-auto p-1 sm:p-1 md:p-2 lg:p-1"
        >
          <div
            class="bg-white rounded-lg shadow-md p-5 flex-1 flex flex-col overflow-hidden"
          >
            <!-- Toolbar -->
            <div
              class="flex flex-wrap items-center gap-2 md:gap-3 pb-4 border-b shrink-0 flex-none sticky top-0 bg-white z-20"
            >
              <!-- Left Section -->
              <div class="flex items-center gap-3">
                <!-- Tambah Perusahaan Button -->
                <button
                  @click="openTambahPerusahaan"
                  class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-white bg-[#6444C6] hover:bg-[#5c3db8] transition text-sm"
                >
                  <PlusIcon class="w-5 h-5" />
                  <span>Tambah Perusahaan Kontraktor</span>
                </button>
              </div>

              <div class="flex items-center gap-3">
                <div class="relative flex min-w-56">
                  <MagnifyingGlassIcon
                    class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
                  />
                  <input
                    v-model="searchQuery"
                    @input="currentPage = 1"
                    type="text"
                    placeholder="Cari nama..."
                    class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-md text-sm text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <!-- Delete Button -->
                <button
                  @click="handleDeleteCompanies"
                  :disabled="selectedRowIds.length === 0 || isLoading"
                  class="flex items-center gap-2 px-3 py-2 rounded-md transition text-sm"
                  :class="
                    selectedRowIds.length > 0 && !isLoading
                      ? 'bg-red-100 text-red-700 border border-red-300 hover:bg-red-200'
                      : 'bg-gray-100 text-gray-400 border border-gray-300 cursor-not-allowed'
                  "
                >
                  <TrashIcon class="w-4 h-4" />
                  <span>{{ isLoading ? "Loading..." : "Hapus" }}</span>
                </button>
              </div>
            </div>

            <!-- Table Container with Horizontal Scroll -->
            <div
              class="flex flex-col gap-4 bg-gray-50 p-1 rounded-lg border border-gray-200 mt-4"
            >
              <!-- Loading & Error Messages -->
              <div v-if="isLoading" class="text-center py-8 text-gray-600">
                <div
                  class="animate-spin inline-block w-8 h-8 border-4 border-current border-t-transparent rounded-full"
                  role="status"
                >
                  <span class="sr-only">Loading...</span>
                </div>
                <p class="mt-2">Memuat data...</p>
              </div>

              <div v-else-if="errorMessage" class="text-center py-8">
                <p class="text-red-600">{{ errorMessage }}</p>
                <button
                  @click="fetchCompanies"
                  class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Coba Lagi
                </button>
              </div>

              <div
                v-else-if="tableData.length === 0"
                class="text-center py-8 text-gray-600"
              >
                <p>Belum ada data perusahaan</p>
              </div>

              <div
                v-else
                class="overflow-x-auto overflow-y-auto rounded-lg border bg-white max-h-[600px]"
              >
                <table class="w-full border-collapse">
                  <thead class="sticky top-0 z-10">
                    <tr class="border-b-2 border-gray-400 bg-gray-50">
                      <th
                        class="px-4 py-3 text-left font-semibold text-gray-700 whitespace-nowrap w-12"
                      >
                        <div
                          class="relative w-5 h-5 shrink-0 flex items-center justify-center"
                        >
                          <input
                            type="checkbox"
                            :checked="selectAllChecked"
                            @change="toggleSelectAll"
                            class="shrink-0 cursor-pointer rounded-md border-2 appearance-none bg-white border-gray-600 checked:bg-blue-500 checked:border-blue-500 box-border"
                            style="
                              width: 1.25rem;
                              height: 1.25rem;
                              appearance: none;
                              -webkit-appearance: none;
                              -moz-appearance: none;
                            "
                            title="Pilih semua / Batal pilih semua"
                          />
                          <CheckIcon
                            v-if="selectAllChecked"
                            class="absolute inset-0 m-auto w-4 h-4 text-white pointer-events-none"
                          />
                        </div>
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap w-20"
                      >
                        No.
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap w-48 cursor-pointer hover:bg-gray-100 transition"
                        @click="sortByCompanyName"
                      >
                        <div class="flex items-center gap-2">
                          <span>Nama Perusahaan</span>
                          <ArrowDownIcon
                            v-if="sortOrder === 'asc'"
                            class="w-4 h-4"
                          />
                          <ArrowUpIcon v-else class="w-4 h-4" />
                        </div>
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap w-28"
                      >
                        Status
                      </th>
                      <th
                        class="px-4 py-3 text-right text-sm font-semibold text-gray-700 whitespace-nowrap flex-1"
                      >
                        Edit
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="row in paginatedData"
                      :key="row.id"
                      class="border-b border-gray-200 hover:bg-gray-50 transition cursor-pointer"
                      :class="{ 'bg-blue-50': isRowSelected(row.id) }"
                    >
                      <td class="px-4 py-3 whitespace-nowrap w-12">
                        <div
                          class="relative w-5 h-5 shrink-0 flex items-center justify-center"
                        >
                          <input
                            type="checkbox"
                            :checked="isRowSelected(row.id)"
                            @change="selectRow(row.id)"
                            @click.stop
                            class="shrink-0 cursor-pointer rounded-md border-2 appearance-none bg-white border-gray-600 checked:bg-blue-500 checked:border-blue-500 box-border"
                            style="
                              width: 1.25rem;
                              height: 1.25rem;
                              appearance: none;
                              -webkit-appearance: none;
                              -moz-appearance: none;
                            "
                          />
                          <CheckIcon
                            v-if="isRowSelected(row.id)"
                            class="absolute inset-0 m-auto w-4 h-4 text-white pointer-events-none"
                          />
                        </div>
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap w-20"
                      >
                        {{ tableData.indexOf(row) + 1 }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap w-48"
                      >
                        {{ row.namaPerusahaan }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap w-28"
                      >
                        {{ row.status }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap flex-1 text-right"
                      >
                        <button
                          @click="openEditPerusahaan(row)"
                          class="p-1 hover:bg-gray-100 rounded transition"
                        >
                          <PencilSquareIcon
                            class="w-4.5 h-4.5 text-black hover:text-blue-800"
                          />
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Pagination -->
              <div
                class="flex flex-wrap justify-between items-center gap-3 pt-4 border-t border-gray-200 bg-white px-2"
              >
                <div class="flex items-center gap-2 text-sm text-gray-700">
                  <span>Tampilkan</span>
                  <select
                    v-model="itemsPerPage"
                    @change="currentPage = 1"
                    class="px-2 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option :value="10">10</option>
                    <option :value="20">20</option>
                    <option :value="50">50</option>
                    <option :value="100">100</option>
                  </select>
                  <span>baris</span>
                </div>
                <div class="flex items-center gap-3">
                  <button
                    @click="previousPage"
                    :disabled="currentPage === 1"
                    class="px-3 py-1 border border-gray-300 rounded-md text-gray-700 font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition"
                  >
                    &lt;
                  </button>
                  <span class="text-sm text-gray-700 font-medium"
                    >{{ startIndex }} - {{ endIndex }} dari
                    {{ filteredTableData.length }}</span
                  >
                  <button
                    @click="nextPage"
                    :disabled="currentPage === totalPages"
                    class="px-3 py-1 border border-gray-300 rounded-md text-gray-700 font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition"
                  >
                    &gt;
                  </button>
                </div>
              </div>
            </div>

            <!-- Konten Tambah Perusahaan -->
            <div
              v-if="showTambahPerusahaan"
              class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            >
              <div
                class="bg-white rounded-lg w-full max-w-md md:max-w-xl max-h-[90vh] overflow-y-auto shadow-[0_4px_6px_rgba(0,0,0,0.1)] p-6 md:p-8"
              >
                <div
                  class="flex justify-between items-center mb-4 pb-3 border-b border-gray-200"
                >
                  <h2 class="text-lg md:text-xl font-semibold text-gray-900">
                    Tambah Perusahaan Kontraktor
                  </h2>
                  <button
                    @click="closeTambahPerusahaan"
                    class="shrink-0 p-1 hover:bg-gray-100 rounded-md transition"
                  >
                    <XMarkIcon
                      class="w-6 h-6 text-gray-600 hover:text-gray-900"
                    />
                  </button>
                </div>

                <!-- Error Message -->
                <div
                  v-if="errorMessage"
                  class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md"
                >
                  <p class="text-sm text-red-600">{{ errorMessage }}</p>
                </div>

                <div>
                  <label
                    class="block text-base font-medium text-black mb-2 mt-4"
                    >Nama Perusahaan <span class="text-red-500">*</span></label
                  >
                  <div class="relative">
                    <input
                      v-model="formData.nama_perusahaan"
                      type="text"
                      placeholder="Masukkan nama"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
                      :disabled="isLoading"
                    />
                    <PencilIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
                    />
                  </div>
                </div>
                <div>
                  <label
                    class="block text-base font-medium text-gray-800 mb-2 mt-2"
                    >Status Perusahaan</label
                  >
                  <div class="relative">
                    <input
                      v-model="formData.status"
                      type="text"
                      placeholder="Pilih status (opsional)"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
                      :disabled="isLoading"
                    />
                    <PencilIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
                    />
                  </div>
                </div>

                <div class="flex justify-end gap-3 mt-6">
                  <button
                    @click="handleTambahPerusahaan"
                    :disabled="isLoading"
                    class="px-6 md:px-6 py-2 text-sm md:text-sm bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ isLoading ? "Menyimpan..." : "Tambah Perusahaan" }}
                  </button>
                  <button
                    @click="closeTambahPerusahaan"
                    :disabled="isLoading"
                    class="px-6 md:px-6 py-2 text-sm md:text-sm border border-gray-300 bg-red-600 text-white rounded-xl hover:bg-red-700 transition font-regular disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Batal
                  </button>
                </div>
              </div>
            </div>

            <!-- Edit Perusahaan -->
            <div
              v-if="showEditPerusahaan"
              class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            >
              <div
                class="bg-white rounded-lg w-full max-w-md md:max-w-xl max-h-[90vh] overflow-y-auto shadow-[0_4px_6px_rgba(0,0,0,0.1)] p-6 md:p-8"
              >
                <div
                  class="flex justify-between items-center mb-4 pb-3 border-b border-gray-200"
                >
                  <h2 class="text-lg md:text-xl font-semibold text-gray-900">
                    Edit Perusahaan Kontraktor
                  </h2>
                  <button
                    @click="closeEditPerusahaan"
                    class="shrink-0 p-1 hover:bg-gray-100 rounded-md transition"
                  >
                    <XMarkIcon
                      class="w-6 h-6 text-gray-600 hover:text-gray-900"
                    />
                  </button>
                </div>

                <!-- Error Message -->
                <div
                  v-if="errorMessage"
                  class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md"
                >
                  <p class="text-sm text-red-600">{{ errorMessage }}</p>
                </div>

                <div>
                  <label
                    class="block text-base font-medium text-black mb-2 mt-4"
                    >Nama Perusahaan <span class="text-red-500">*</span></label
                  >
                  <div class="relative">
                    <input
                      v-model="formData.nama_perusahaan"
                      type="text"
                      placeholder="Masukkan nama"
                      class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
                      :disabled="isLoading"
                    />
                    <PencilSquareIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
                    />
                  </div>
                </div>
                <div>
                  <label
                    class="block text-base font-medium text-gray-800 mb-2 mt-2"
                    >Status Perusahaan</label
                  >
                  <div class="relative">
                    <input
                      v-model="formData.status"
                      type="text"
                      placeholder="Pilih status (opsional)"
                      class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
                      :disabled="isLoading"
                    />
                    <PencilSquareIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
                    />
                  </div>
                </div>

                <div class="flex justify-end gap-3 mt-6">
                  <button
                    @click="handleEditPerusahaan"
                    :disabled="isLoading"
                    class="px-6 md:px-6 py-2 text-sm md:text-sm bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ isLoading ? "Menyimpan..." : "Edit Perusahaan" }}
                  </button>
                  <button
                    @click="closeEditPerusahaan"
                    :disabled="isLoading"
                    class="px-6 md:px-6 py-2 text-sm md:text-sm border border-gray-300 bg-red-600 text-white rounded-xl hover:bg-red-700 transition font-regular disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Batal
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>
