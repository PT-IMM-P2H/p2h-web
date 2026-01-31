<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import Aside from "../../bar/aside.vue";
import HeaderAdmin from "../../bar/header_admin.vue";
import BulkUploadModal from "../BulkUploadModal.vue";
import ExportDropdown from "../ExportDropdown.vue";
import {
  MagnifyingGlassIcon,
  Bars3BottomLeftIcon,
  ArrowUpTrayIcon,
  ArrowDownTrayIcon,
  TrashIcon,
  UserPlusIcon,
  CloudArrowUpIcon,
  PencilSquareIcon,
  XMarkIcon,
  ChevronDownIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  CheckIcon,
} from "@heroicons/vue/24/outline";
import { PencilIcon, CalendarIcon } from "@heroicons/vue/24/solid";
import apiService from "@/services/api";
import { useSidebarProvider } from "../../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();

const router = useRouter();

const selectedRowIds = ref([]);
const selectAllChecked = ref(false);
const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = ref(10);
const tambahPengguna = ref(false);
const showFilter = ref(false);
const sortOrder = ref("asc");
const isLoading = ref(false);
const errorMessage = ref("");
const editingId = ref(null);
const showBulkUpload = ref(false);
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const filterData = ref({
  departemen: "",
  posisi: "",
  status: "",
  namaPerusahaan: "",
});
const appliedFilterData = ref({
  departemen: "",
  posisi: "",
  status: "",
  namaPerusahaan: "",
});

const opentambahPengguna = () => {
  editingId.value = null;
  formData.value = {
    full_name: "",
    phone_number: "",
    email: "",
    company_id: "",
    department_id: "",
    position_id: "",
    work_status_id: "",
    birth_date: "",
    role: "",
    kategori_pengguna: "",
  };
  tambahPengguna.value = true;
};

const closeTambahPengguna = () => {
  editingId.value = null;
  formData.value = {
    full_name: "",
    phone_number: "",
    email: "",
    company_id: "",
    department_id: "",
    position_id: "",
    work_status_id: "",
    birth_date: "",
    role: "",
    kategori_pengguna: "",
  };
  tambahPengguna.value = false;
};

const openFilter = () => {
  showFilter.value = true;
};

const closeFilter = () => {
  showFilter.value = false;
};

const applyFilter = () => {
  appliedFilterData.value = { ...filterData.value };
  currentPage.value = 1;
  closeFilter();
};

const openBulkUpload = () => {
  showBulkUpload.value = true;
};

const closeBulkUpload = () => {
  showBulkUpload.value = false;
};

const handleUploadSuccess = () => {
  fetchUsers();
};

const exportFilters = computed(() => ({
  kategori: "TRAVEL",
  role: appliedFilterData.value.role || undefined,
  is_active: true, // Selalu export hanya user aktif (sesuai yang ditampilkan di tabel)
  search: searchQuery.value || undefined,
}));

const tableData = ref([]);

// Master data untuk dropdown
const companies = ref([]);
const departments = ref([]);
const positions = ref([]);
const statuses = ref([]);
const roles = [
  { value: "user", label: "User" },
  { value: "admin", label: "Admin" },
  { value: "superadmin", label: "Superadmin" },
];

// Form data untuk tambah/edit pengguna
const formData = ref({
  full_name: "",
  phone_number: "",
  email: "",
  company_id: "",
  department_id: "",
  position_id: "",
  work_status_id: "",
  birth_date: "",
  role: "",
  kategori_pengguna: "",
});

// Fetch master data
const fetchMasterData = async () => {
  try {
    const [companiesRes, departmentsRes, positionsRes, statusesRes] =
      await Promise.all([
        apiService.master.getCompanies(),
        apiService.master.getDepartments(),
        apiService.master.getPositions(),
        apiService.master.getStatuses(),
      ]);

    if (companiesRes.data.status === "success" || companiesRes.data.success) {
      companies.value = companiesRes.data.payload;
    }
    if (
      departmentsRes.data.status === "success" ||
      departmentsRes.data.success
    ) {
      departments.value = departmentsRes.data.payload;
    }
    if (positionsRes.data.status === "success" || positionsRes.data.success) {
      positions.value = positionsRes.data.payload;
    }
    if (statusesRes.data.status === "success" || statusesRes.data.success) {
      statuses.value = statusesRes.data.payload;
    }
  } catch (error) {
    console.error("Error fetching master data:", error);
  } finally {
    // Cleanup if needed
  }
};

// Fetch users dari backend (filter kategori TRAVEL)
const fetchUsers = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const response = await apiService.users.getAll({ limit: 2000 });

    if (response.data.status === "success" || response.data.success) {
      // Filter hanya user dengan kategori TRAVEL dan is_active = true
      const allUsers = response.data.payload;
      const travelUsers = allUsers.filter(
        (user) =>
          user.kategori_pengguna === "TRAVEL" && user.is_active === true,
      );

      tableData.value = travelUsers.map((user) => ({
        id: user.id,
        namaLengkap: user.full_name,
        noHandphone: user.phone_number,
        email: user.email,
        namaPerusahaan: user.company?.nama_perusahaan || "-",
        departemen: user.department?.nama_department || "-",
        posisi: user.position?.nama_posisi || "-",
        status: user.work_status?.nama_status || "-",
        birth_date: user.birth_date,
        role: user.role,
      }));
    } else {
      errorMessage.value = response.data.message || "Gagal mengambil data";
    }
  } catch (error) {
    console.error("Error fetching users:", error);
    errorMessage.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Gagal mengambil data pengguna";
  } finally {
    isLoading.value = false;
  }
};

// Hapus pengguna (soft delete)
const handleDeleteUsers = async () => {
  if (selectedRowIds.value.length === 0) {
    alert("Pilih pengguna yang ingin dihapus!");
    return;
  }

  if (
    !confirm(`Yakin ingin menghapus ${selectedRowIds.value.length} pengguna?`)
  ) {
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";
  let deletedCount = 0;
  let failedCount = 0;

  try {
    // Try bulk delete first (faster for many items)
    if (selectedRowIds.value.length > 5) {
      try {
        await apiService.users.bulkDelete(selectedRowIds.value);
        deletedCount = selectedRowIds.value.length;
      } catch (bulkError) {
        console.warn(
          "Bulk delete not supported, falling back to parallel delete:",
          bulkError,
        );
        // Fallback to parallel delete
        const deletePromises = selectedRowIds.value.map(async (id) => {
          try {
            await apiService.users.delete(id);
            return { success: true, id };
          } catch (err) {
            return { success: false, id, error: err };
          }
        });

        const results = await Promise.all(deletePromises);
        deletedCount = results.filter((r) => r.success).length;
        failedCount = results.filter((r) => !r.success).length;
      }
    } else {
      // For small batches (<= 5), use parallel delete
      const deletePromises = selectedRowIds.value.map(async (id) => {
        try {
          await apiService.users.delete(id);
          return { success: true, id };
        } catch (err) {
          return { success: false, id, error: err };
        }
      });

      const results = await Promise.all(deletePromises);
      deletedCount = results.filter((r) => r.success).length;
      failedCount = results.filter((r) => !r.success).length;
    }

    selectedRowIds.value = [];
    selectAllChecked.value = false;
    tableData.value = [];

    await fetchUsers();

    if (failedCount > 0) {
      alert(
        `Berhasil: ${deletedCount} pengguna\nGagal: ${failedCount} pengguna`,
      );
    } else {
      alert(`${deletedCount} pengguna berhasil dihapus`);
    }
  } catch (error) {
    console.error("Error deleting users:", error);
    errorMessage.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Gagal menghapus pengguna";
    alert(
      `Error: ${errorMessage.value}\n\nBerhasil dihapus: ${deletedCount} dari ${selectedRowIds.value.length}`,
    );
  } finally {
    isLoading.value = false;
  }
};

// Submit tambah/edit pengguna
const handleTambahPengguna = async () => {
  // Validasi field wajib
  if (!formData.value.full_name || !formData.value.phone_number) {
    alert("Nama lengkap dan nomor telepon wajib diisi!");
    return;
  }

  // Validasi birth_date jika password tidak diisi (untuk auto-generate)
  if (!formData.value.password && !formData.value.birth_date) {
    alert(
      "Tanggal lahir wajib diisi untuk membuat password otomatis!\n\n" +
        "Format password: namadepan + DDMMYYYY\n" +
        "Contoh: Yunnifa Nur Lailli lahir 12/06/2003 → yunnifa12062003",
    );
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";

  try {
    let response;

    // Prepare payload - ensure kategori is TRAVEL for this page
    const payload = {
      ...formData.value,
      kategori_pengguna: "TRAVEL", // Force TRAVEL for Travel page
      email: formData.value.email || null, // Convert empty string to null
      birth_date: formData.value.birth_date || null,
      company_id: formData.value.company_id || null,
      department_id: formData.value.department_id || null,
      position_id: formData.value.position_id || null,
      work_status_id: formData.value.work_status_id || null,
    };

    console.log(
      "📤 Sending user payload (Travel):",
      JSON.stringify(payload, null, 2),
    );

    if (editingId.value) {
      response = await apiService.users.update(editingId.value, payload);
    } else {
      response = await apiService.users.create(payload);
    }

    if (response.data.status === "success" || response.data.success) {
      alert(
        editingId.value
          ? "Pengguna berhasil diupdate"
          : "Pengguna berhasil ditambahkan",
      );

      editingId.value = null;
      formData.value = {
        full_name: "",
        phone_number: "",
        email: "",
        company_id: "",
        department_id: "",
        position_id: "",
        work_status_id: "",
        birth_date: "",
        role: "user",
        kategori_pengguna: "TRAVEL",
      };

      closeTambahPengguna();
      await fetchUsers();
    } else {
      errorMessage.value =
        response.data.message || "Gagal menyimpan data pengguna";
      alert(errorMessage.value);
    }
  } catch (error) {
    console.error("Error saving user:", error);
    errorMessage.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Gagal menyimpan data pengguna";
    alert(`Error: ${errorMessage.value}`);
  } finally {
    isLoading.value = false;
  }
};

// Edit pengguna
const editPengguna = async (rowId) => {
  try {
    const response = await apiService.users.getById(rowId);

    if (response.data.status === "success" || response.data.success) {
      const user = response.data.payload;

      editingId.value = rowId;
      formData.value = {
        full_name: user.full_name || "",
        phone_number: user.phone_number || "",
        email: user.email || "",
        company_id: user.company_id || "",
        department_id: user.department_id || "",
        position_id: user.position_id || "",
        work_status_id: user.work_status_id || "",
        birth_date: user.birth_date || "",
        role: user.role || "user",
        kategori_pengguna: "TRAVEL",
      };

      tambahPengguna.value = true;
    }
  } catch (error) {
    console.error("Error fetching user detail:", error);
    alert("Gagal mengambil data pengguna");
  } finally {
    // Cleanup if needed
  }
};

// Load data saat component di-mount
onMounted(() => {
  fetchUsers();
  fetchMasterData();
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
  if (!str) return "";
  return str.toLowerCase().replace(/[\s\-./]/g, "");
};

// Filter data berdasarkan search query dan filter yang diterapkan
const filteredTableData = computed(() => {
  let filtered = tableData.value;

  // Filter berdasarkan search query
  if (searchQuery.value.trim()) {
    const query = normalizeString(searchQuery.value);
    filtered = filtered.filter((row) => {
      return (
        normalizeString(row.namaLengkap || "").includes(query) ||
        normalizeString(row.email || "").includes(query) ||
        normalizeString(row.noHandphone || "").includes(query) ||
        normalizeString(row.namaPerusahaan || "").includes(query) ||
        normalizeString(row.departemen || "").includes(query) ||
        normalizeString(row.posisi || "").includes(query) ||
        normalizeString(row.status || "").includes(query)
      );
    });
  }

  // Filter berdasarkan filter yang diterapkan
  if (appliedFilterData.value.departemen) {
    filtered = filtered.filter(
      (row) => row.departemen === appliedFilterData.value.departemen,
    );
  }
  if (appliedFilterData.value.posisi) {
    filtered = filtered.filter(
      (row) => row.posisi === appliedFilterData.value.posisi,
    );
  }
  if (appliedFilterData.value.status) {
    filtered = filtered.filter(
      (row) => row.status === appliedFilterData.value.status,
    );
  }
  if (appliedFilterData.value.namaPerusahaan) {
    filtered = filtered.filter(
      (row) => row.namaPerusahaan === appliedFilterData.value.namaPerusahaan,
    );
  }

  return filtered;
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

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const sortByName = () => {
  if (sortOrder.value === "asc") {
    sortOrder.value = "desc";
    tableData.value = [...tableData.value].sort((a, b) =>
      b.namaLengkap.localeCompare(a.namaLengkap),
    );
  } else {
    sortOrder.value = "asc";
    tableData.value = [...tableData.value].sort((a, b) =>
      a.namaLengkap.localeCompare(b.namaLengkap),
    );
  }
  currentPage.value = 1;
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
          <!-- Judul -->
          <div class="mb-2 shrink-0 sticky top-0 z-30 bg-[#EFEFEF]">
            <div class="bg-white rounded-lg shadow-md p-1 pl-5">
              <h1 class="text-base font-bold text-[#523E95] text-left">
                Travel
              </h1>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow-md p-5 flex flex-col relative">
            <!-- Toolbar - Sticky -->
            <div
              class="flex flex-wrap items-center gap-2 md:gap-3 pb-4 border-b shrink-0 flex-none sticky top-14 bg-white z-20"
            >
              <!-- Left Section -->
              <div class="flex items-center gap-2 md:gap-3 order-1">
                <!-- Tambah pengguna Button -->
                <button
                  @click="opentambahPengguna"
                  class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-white bg-[#6444C6] hover:bg-[#5c3db8] transition text-sm"
                >
                  <UserPlusIcon class="w-5 h-5" />
                  <span class="hidden sm:inline">Tambah Pengguna</span>
                </button>

                <!-- Upload button -->
                <button
                  @click="openBulkUpload"
                  class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition text-sm"
                >
                  <CloudArrowUpIcon class="w-4 h-4" />
                  <span class="hidden sm:inline">Upload</span>
                </button>
              </div>

              <!-- Search - Full width on mobile -->
              <div
                class="relative flex w-full md:w-auto md:min-w-50 order-3 md:order-2"
              >
                <MagnifyingGlassIcon
                  class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
                />
                <input
                  id="search-pengguna-travel"
                  name="search"
                  v-model="searchQuery"
                  @input="currentPage = 1"
                  type="text"
                  placeholder="Cari nama..."
                  aria-label="Cari pengguna Travel"
                  class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-md text-sm text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <!-- Right Section -->
              <div
                class="flex items-center gap-2 md:gap-3 order-2 md:order-3 ml-auto"
              >
                <!-- Filter Button -->
                <button
                  @click="openFilter"
                  class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition text-sm"
                >
                  <Bars3BottomLeftIcon class="w-4 h-4" />
                  <span class="hidden sm:inline">Filter</span>
                </button>

                <!-- Export Dropdown -->
                <div>
                  <ExportDropdown
                    :export-endpoint="`${API_BASE_URL}/export/users`"
                    :filters="exportFilters"
                  />
                </div>

                <!-- Delete Button -->
                <button
                  @click="handleDeleteUsers"
                  :disabled="selectedRowIds.length === 0 || isLoading"
                  class="flex items-center gap-2 px-3 py-2 rounded-md transition text-sm"
                  :class="
                    selectedRowIds.length > 0 && !isLoading
                      ? 'bg-red-100 text-red-700 border border-red-300 hover:bg-red-200'
                      : 'bg-gray-100 text-gray-400 border border-gray-300 cursor-not-allowed'
                  "
                >
                  <TrashIcon class="w-4 h-4" />
                  <span class="hidden sm:inline">{{
                    isLoading ? "Loading..." : "Hapus"
                  }}</span>
                </button>
              </div>
            </div>

            <!-- Table Container with Horizontal Scroll -->
            <div
              class="flex flex-col flex-1 bg-gray-50 p-1 rounded-lg border border-gray-200 mt-4 min-h-0"
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
                  @click="fetchUsers"
                  class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Coba Lagi
                </button>
              </div>

              <div
                v-else-if="tableData.length === 0"
                class="text-center py-8 text-gray-600"
              >
                <p>Belum ada data pengguna</p>
              </div>

              <div
                v-else
                class="overflow-x-auto overflow-y-auto rounded-lg border bg-white max-h-[500px]"
              >
                <table class="w-full border-collapse">
                  <thead class="sticky top-0 z-10">
                    <tr class="border-b-2 border-gray-400 bg-gray-50">
                      <th
                        class="px-2 md:px-3 py-3 text-center font-semibold text-gray-700 whitespace-nowrap w-10 md:w-12"
                      >
                        <div class="flex justify-center items-center">
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
                        </div>
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-32 cursor-pointer hover:bg-gray-100 transition"
                        @click="sortByName"
                      >
                        <div class="flex items-center gap-2">
                          <span>Nama Lengkap</span>
                          <ArrowDownIcon
                            v-if="sortOrder === 'asc'"
                            class="w-4 h-4"
                          />
                          <ArrowUpIcon v-else class="w-4 h-4" />
                        </div>
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-24"
                      >
                        No. Handphone
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Email
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Nama Perusahaan
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Departemen
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-20"
                      >
                        Posisi
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-20"
                      >
                        Status
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Tanggal Lahir
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-16"
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
                      <td
                        class="px-2 md:px-3 py-3 whitespace-nowrap text-center w-10 md:w-12"
                      >
                        <div class="flex justify-center items-center">
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
                        </div>
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 whitespace-nowrap min-w-32 text-xs"
                      >
                        {{ row.namaLengkap }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-24"
                      >
                        {{ row.noHandphone }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-24"
                      >
                        {{ row.email }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.namaPerusahaan }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.departemen }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-20"
                      >
                        {{ row.posisi }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-20"
                      >
                        {{ row.status }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{
                          row.birth_date
                            ? new Date(row.birth_date).toLocaleDateString(
                                "id-ID",
                              )
                            : "-"
                        }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-16"
                      >
                        <button
                          @click="editPengguna(row.id)"
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
            </div>

            <!-- Pagination - Fixed at bottom -->
            <div
              class="flex flex-wrap justify-between items-center gap-3 py-3 px-4 border-t border-gray-200 bg-white rounded-b-lg mt-2 shrink-0"
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
                  <option :value="500">500</option>
                  <option :value="1000">1000</option>
                  <option :value="1500">1500</option>
                  <option :value="2000">2000</option>
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
                <span class="text-sm text-gray-700 font-medium">
                  {{ startIndex }} - {{ endIndex }} dari
                  {{ filteredTableData.length }}
                </span>
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages"
                  class="px-3 py-1 border border-gray-300 rounded-md text-gray-700 font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition"
                >
                  &gt;
                </button>
              </div>
            </div>

            <!-- Konten Tambah pengguna -->
            <div
              v-if="tambahPengguna"
              class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            >
              <div
                class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-[0_4px_6px_rgba(0,0,0,0.1)] p-6 md:p-8"
              >
                <div
                  class="flex justify-between items-center mb-1 pb-3 border-b border-gray-200"
                >
                  <h2 class="text-lg md:text-xl font-semibold text-gray-900">
                    {{
                      editingId
                        ? "Edit Pengguna Travel"
                        : "Tambah Pengguna Travel"
                    }}
                  </h2>
                  <button
                    @click="closeTambahPengguna"
                    class="shrink-0 p-1 hover:bg-gray-100 rounded-md transition"
                  >
                    <XMarkIcon
                      class="w-6 h-6 text-gray-600 hover:text-gray-900"
                    />
                  </button>
                </div>

                <!-- Row 1: Nama Lengkap dan Nomor Telepon -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label
                      for="full_name_travel"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Nama Lengkap</label
                    >
                    <div class="relative">
                      <input
                        id="full_name_travel"
                        name="full_name"
                        v-model="formData.full_name"
                        type="text"
                        placeholder="Masukkan nama"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                      />
                      <PencilIcon
                        class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                      />
                    </div>
                  </div>

                  <div>
                    <label
                      for="phone_number_travel"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Nomor Telepon</label
                    >
                    <div class="relative">
                      <input
                        id="phone_number_travel"
                        name="phone_number"
                        v-model="formData.phone_number"
                        type="text"
                        placeholder="081xxxxxxxx"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                      />
                      <PencilIcon
                        class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                      />
                    </div>
                  </div>
                </div>

                <!-- Row 2: Email dan Nama Perusahaan -->
                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label
                      for="email_travel"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Email</label
                    >
                    <div class="relative">
                      <input
                        id="email_travel"
                        name="email"
                        v-model="formData.email"
                        type="email"
                        placeholder="email@example.com"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                      />
                      <PencilIcon
                        class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                      />
                    </div>
                  </div>

                  <div>
                    <label
                      for="company_id_travel"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Nama Perusahaan</label
                    >
                    <div class="relative">
                      <select
                        id="company_id_travel"
                        name="company_id"
                        v-model="formData.company_id"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm appearance-none"
                      >
                        <option value="">Pilih nama perusahaan</option>
                        <option
                          v-for="company in companies"
                          :key="company.id"
                          :value="company.id"
                        >
                          {{ company.nama_perusahaan }}
                        </option>
                      </select>
                      <ChevronDownIcon
                        class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                      />
                    </div>
                  </div>
                </div>

                <!-- Row 3: Departemen dan Posisi -->
                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label
                      for="department_id_travel"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Departemen</label
                    >
                    <div class="relative">
                      <select
                        id="department_id_travel"
                        name="department_id"
                        v-model="formData.department_id"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm appearance-none"
                      >
                        <option value="">Pilih departemen</option>
                        <option
                          v-for="dept in departments"
                          :key="dept.id"
                          :value="dept.id"
                        >
                          {{ dept.nama_department }}
                        </option>
                      </select>
                      <ChevronDownIcon
                        class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                      />
                    </div>
                  </div>
                  <div>
                    <label
                      for="position_id_travel"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Posisi</label
                    >
                    <div class="relative">
                      <select
                        id="position_id_travel"
                        name="position_id"
                        v-model="formData.position_id"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm appearance-none"
                      >
                        <option value="">Pilih posisi</option>
                        <option
                          v-for="pos in positions"
                          :key="pos.id"
                          :value="pos.id"
                        >
                          {{ pos.nama_posisi }}
                        </option>
                      </select>
                      <ChevronDownIcon
                        class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                      />
                    </div>
                  </div>
                </div>

                <!-- Row 4: Status Pekerjaan dan Tanggal Lahir -->
                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label
                      for="work_status_id_travel"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Status Pekerjaan</label
                    >
                    <div class="relative">
                      <select
                        id="work_status_id_travel"
                        name="work_status_id"
                        v-model="formData.work_status_id"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm appearance-none"
                      >
                        <option value="">Pilih status pekerjaan</option>
                        <option
                          v-for="status in statuses"
                          :key="status.id"
                          :value="status.id"
                        >
                          {{ status.nama_status }}
                        </option>
                      </select>
                      <ChevronDownIcon
                        class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                      />
                    </div>
                  </div>
                  <div>
                    <label
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Tanggal Lahir</label
                    >
                    <input
                      v-model="formData.birth_date"
                      type="date"
                      class="w-full p-2 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                    />
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Role</label
                    >
                    <div class="relative">
                      <select
                        v-model="formData.role"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm appearance-none"
                      >
                        <option value="">Pilih role</option>
                        <option
                          v-for="role in roles"
                          :key="role.value"
                          :value="role.value"
                        >
                          {{ role.label }}
                        </option>
                      </select>
                      <ChevronDownIcon
                        class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                      />
                    </div>
                  </div>
                </div>

                <div class="flex justify-end gap-3 mt-6">
                  <button
                    @click="handleTambahPengguna"
                    :disabled="isLoading"
                    class="px-6 md:px-6 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular disabled:opacity-50"
                  >
                    {{
                      isLoading
                        ? "Loading..."
                        : editingId
                          ? "Update Pengguna"
                          : "Tambah Pengguna"
                    }}
                  </button>
                  <button
                    @click="closeTambahPengguna"
                    class="px-6 md:px-6 py-2 text-sm md:text-base border border-gray-300 bg-red-600 text-white rounded-xl hover:bg-red-700 transition font-regular"
                  >
                    Batal
                  </button>
                </div>
              </div>
            </div>

            <!-- Filter Pengguna -->
            <div
              v-if="showFilter"
              class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            >
              <div
                class="bg-white rounded-lg w-full max-w-md md:max-w-lg max-h-[90vh] overflow-y-auto shadow-[0_4px_6px_rgba(0,0,0,0.1)] p-6 md:p-8"
              >
                <div
                  class="flex justify-between items-center mb-1 pb-3 border-b border-gray-200"
                >
                  <h2 class="text-lg md:text-xl font-semibold text-gray-900">
                    Filter Data
                  </h2>
                  <button
                    @click="closeFilter"
                    class="shrink-0 p-1 hover:bg-gray-100 rounded-md transition"
                  >
                    <XMarkIcon
                      class="w-6 h-6 text-gray-600 hover:text-gray-900"
                    />
                  </button>
                </div>

                <!-- Perusahaan -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Nama Perusahaan</label
                  >
                  <div class="relative">
                    <select
                      v-model="filterData.namaPerusahaan"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] appearance-none"
                    >
                      <option value="">Semua Perusahaan</option>
                      <option
                        v-for="company in companies"
                        :key="company.id"
                        :value="company.nama_perusahaan"
                      >
                        {{ company.nama_perusahaan }}
                      </option>
                    </select>
                    <ChevronDownIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                    />
                  </div>
                </div>

                <!-- Departemen -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Departemen</label
                  >
                  <div class="relative">
                    <select
                      v-model="filterData.departemen"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] appearance-none"
                    >
                      <option value="">Semua Departemen</option>
                      <option
                        v-for="dept in departments"
                        :key="dept.id"
                        :value="dept.nama_department"
                      >
                        {{ dept.nama_department }}
                      </option>
                    </select>
                    <ChevronDownIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                    />
                  </div>
                </div>

                <!-- Posisi Kerja -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Posisi Kerja</label
                  >
                  <div class="relative">
                    <select
                      v-model="filterData.posisi"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] appearance-none"
                    >
                      <option value="">Semua Posisi</option>
                      <option
                        v-for="pos in positions"
                        :key="pos.id"
                        :value="pos.nama_posisi"
                      >
                        {{ pos.nama_posisi }}
                      </option>
                    </select>
                    <ChevronDownIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                    />
                  </div>
                </div>

                <!-- Status Kerja -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Status Kerja</label
                  >
                  <div class="relative">
                    <select
                      v-model="filterData.status"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] appearance-none"
                    >
                      <option value="">Semua Status</option>
                      <option
                        v-for="status in statuses"
                        :key="status.id"
                        :value="status.nama_status"
                      >
                        {{ status.nama_status }}
                      </option>
                    </select>
                    <ChevronDownIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                    />
                  </div>
                </div>

                <div class="flex justify-center gap-3 mt-6">
                  <button
                    @click="closeFilter"
                    class="px-6 md:px-6 py-2 text-sm md:text-base border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition font-regular"
                  >
                    Batal
                  </button>
                  <button
                    @click="applyFilter"
                    class="px-6 md:px-6 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular"
                  >
                    Terapkan
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- Bulk Upload Modal -->
    <BulkUploadModal
      :is-open="showBulkUpload"
      title="Upload Data Pengguna Travel"
      upload-type="users"
      :upload-endpoint="`${API_BASE_URL}/bulk-upload/users`"
      :template-endpoint="`${API_BASE_URL}/bulk-upload/templates/users`"
      @close="closeBulkUpload"
      @success="handleUploadSuccess"
    />
  </div>
</template>
