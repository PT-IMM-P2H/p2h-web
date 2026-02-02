<script setup>
import { ref, computed, onMounted } from "vue";
import Aside from "../../bar/aside.vue";
import HeaderAdmin from "../../bar/header_admin.vue";
import ExportDropdown from "../ExportDropdown.vue";
import {
  MagnifyingGlassIcon,
  Bars3BottomLeftIcon,
  ArrowUpTrayIcon,
  TrashIcon,
  XMarkIcon,
  ChevronDownIcon,
  CalendarIcon,
  CheckIcon,
} from "@heroicons/vue/24/outline";
import { api } from "../../../services/api";
import { useSidebarProvider } from "../../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();

// Export endpoint (relative path - api.js handles base URL)

const selectedRowIds = ref([]);
const selectAllChecked = ref(false);
const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = ref(10);
const showFilter = ref(false);
const isLoading = ref(false);
const filterHasil = ref({
  normal: false,
  abnormal: false,
  warning: false,
});
const appliedFilterHasil = ref({
  normal: false,
  abnormal: false,
  warning: false,
});

// Filter Date & Metadata State
const filterDate = ref({
  start: "",
  end: "",
});
const appliedFilterDate = ref({
  start: "",
  end: "",
});

const filterData = ref({
  namaPerusahaan: "",
  departemen: "",
  posisi: "",
  status: "",
});
const appliedFilterData = ref({
  namaPerusahaan: "",
  departemen: "",
  posisi: "",
  status: "",
});

// Data P2H Reports dari backend
const p2hReports = ref([]);

// Fetch data P2H reports
const fetchP2HReports = async () => {
  try {
    isLoading.value = true;
    console.log("🔄 [Admin] Fetching P2H reports...");
    const response = await api.get("/p2h/reports?limit=100");
    console.log("✅ [Admin] P2H reports fetched:", response.data);
    p2hReports.value = response.data.payload;
    console.log("📊 [Admin] Total reports:", p2hReports.value.length);
  } catch (error) {
    console.error("❌ [Admin] Gagal fetch P2H reports:", error);
    console.error("Error details:", error.response?.data);
    if (error.response?.status === 401) {
      alert("Sesi Anda telah berakhir. Silakan login kembali.");
    } else {
      alert(
        "Gagal memuat data P2H: " +
          (error.response?.data?.detail || error.message),
      );
    }
  } finally {
    isLoading.value = false;
  }
};

// Computed Options for Dropdowns
const companies = computed(() => {
  const unique = new Set();
  const list = [];
  p2hReports.value.forEach((r) => {
    const val = r.user?.company?.nama_perusahaan;
    if (val && !unique.has(val)) {
      unique.add(val);
      list.push({ id: val, nama_perusahaan: val });
    }
  });
  return list.sort((a, b) =>
    a.nama_perusahaan.localeCompare(b.nama_perusahaan),
  );
});

const departments = computed(() => {
  const unique = new Set();
  const list = [];
  p2hReports.value.forEach((r) => {
    const val = r.user?.department?.nama_department;
    if (val && !unique.has(val)) {
      unique.add(val);
      list.push({ id: val, nama_department: val });
    }
  });
  return list.sort((a, b) =>
    a.nama_department.localeCompare(b.nama_department),
  );
});

const positions = computed(() => {
  const unique = new Set();
  const list = [];
  p2hReports.value.forEach((r) => {
    const val = r.user?.position?.nama_posisi;
    if (val && !unique.has(val)) {
      unique.add(val);
      list.push({ id: val, nama_posisi: val });
    }
  });
  return list.sort((a, b) => a.nama_posisi.localeCompare(b.nama_posisi));
});

// Assuming 'job_level' or 'employment_status' maps to 'status'
// Adjust property access based on actual API response structure if needed.
const statuses = computed(() => {
  const unique = new Set();
  const list = [];
  p2hReports.value.forEach((r) => {
    // Fallback check for common status fields
    const val = r.user?.job_level || r.user?.employment_status;
    if (val && !unique.has(val)) {
      unique.add(val);
      list.push({ id: val, nama_status: val });
    }
  });
  return list.sort((a, b) => a.nama_status.localeCompare(b.nama_status));
});

// Format data dari backend ke format tabel
const tableData = computed(() => {
  // Filter hanya data dengan kategori IMM (Operasional PT)
  const filteredReports = p2hReports.value.filter(
    (report) => report.user.kategori_pengguna === "IMM",
  );

  return filteredReports.map((report) => {
    // Extract keterangan dari items yang abnormal/warning (hanya isi keterangan)
    const problemItems = (report.details || []).filter(
      (d) => d.status === "abnormal" || d.status === "warning",
    );

    // Group keterangan by category (section_name)
    const keteranganByCategory = {};
    problemItems
      .filter((d) => d.keterangan && d.keterangan.trim())
      .forEach((d) => {
        const category = d.checklist_item.section_name;
        if (!keteranganByCategory[category]) {
          keteranganByCategory[category] = [];
        }
        keteranganByCategory[category].push(d.keterangan.trim());
      });

    const hasKeterangan = Object.keys(keteranganByCategory).length > 0;

    // Format shift number menjadi shift name
    let shiftName = `Shift ${report.shift_number}`;
    if (report.vehicle.shift_type === "non_shift") {
      shiftName = "Non Shift";
    } else if (report.shift_number === 4) {
      shiftName = "Long Shift";
    }

    return {
      id: report.id,
      tanggal: report.submission_date,
      waktu: report.submission_time,
      shift: shiftName,
      shiftRaw: report.shift_number,
      noLambung: report.vehicle.no_lambung,
      nomorPolisi: report.vehicle.plat_nomor || "-",
      warnaLambung: report.vehicle.warna_no_lambung || "-",
      tipe: report.vehicle.vehicle_type,
      merek: report.vehicle.merk || "-",
      namaPemeriksa: report.user.full_name,
      kategoriLayanan: "Operasional PT",
      perusahaan: report.user.company?.nama_perusahaan || "-",
      departemen: report.user.department?.nama_department || "-",
      posisi: report.user.position?.nama_posisi || "-",
      statusKerja:
        report.user.job_level || report.user.employment_status || "-",
      hasil:
        report.overall_status === "normal"
          ? "Normal"
          : report.overall_status === "warning"
            ? "Warning"
            : "Abnormal",
      hasilRaw: report.overall_status,
      keteranganByCategory: keteranganByCategory,
      hasKeterangan: hasKeterangan,
    };
  });
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

const isIndeterminate = () => {
  const selectedCount = selectedRowIds.value.length;
  return selectedCount > 0 && selectedCount < tableData.value.length;
};

const getResultColor = (hasil) => {
  const styles = {
    Normal: { bg: "#A7E8BF", text: "#1A5C3F" },
    Abnormal: { bg: "#F7E19C", text: "#8B6F47" },
    Warning: { bg: "#FFA0A0", text: "#8B3A3A" },
  };
  return styles[hasil] || styles["Normal"];
};

// Helper function untuk normalize string (hapus whitespace dan karakter khusus)
const normalizeString = (str) => {
  return str.toLowerCase().replace(/[\s\-./]/g, "");
};

// Filter data berdasarkan search query dan hasil
const filteredTableData = computed(() => {
  let filtered = tableData.value;

  // Filter berdasarkan search query
  if (searchQuery.value.trim()) {
    const query = normalizeString(searchQuery.value);
    filtered = filtered.filter((row) => {
      return (
        normalizeString(row.namaPemeriksa).includes(query) ||
        normalizeString(row.noLambung).includes(query) ||
        normalizeString(row.nomorPolisi).includes(query) ||
        normalizeString(row.merek).includes(query)
      );
    });
  }

  // Filter berdasarkan Date Range
  if (appliedFilterDate.value.start && appliedFilterDate.value.end) {
    const startDate = new Date(appliedFilterDate.value.start);
    const endDate = new Date(appliedFilterDate.value.end);
    // Reset time parts for accurate comparison
    startDate.setHours(0, 0, 0, 0);
    endDate.setHours(23, 59, 59, 999);

    filtered = filtered.filter((row) => {
      const rowDate = new Date(row.tanggal);
      return rowDate >= startDate && rowDate <= endDate;
    });
  } else if (appliedFilterDate.value.start) {
    const startDate = new Date(appliedFilterDate.value.start);
    startDate.setHours(0, 0, 0, 0);
    filtered = filtered.filter((row) => new Date(row.tanggal) >= startDate);
  } else if (appliedFilterDate.value.end) {
    const endDate = new Date(appliedFilterDate.value.end);
    endDate.setHours(23, 59, 59, 999);
    filtered = filtered.filter((row) => new Date(row.tanggal) <= endDate);
  }

  // Filter Company
  if (appliedFilterData.value.namaPerusahaan) {
    filtered = filtered.filter(
      (row) => row.perusahaan === appliedFilterData.value.namaPerusahaan,
    );
  }

  // Filter Department
  if (appliedFilterData.value.departemen) {
    filtered = filtered.filter(
      (row) => row.departemen === appliedFilterData.value.departemen,
    );
  }

  // Filter Position
  if (appliedFilterData.value.posisi) {
    filtered = filtered.filter(
      (row) => row.posisi === appliedFilterData.value.posisi,
    );
  }

  // Filter Status
  if (appliedFilterData.value.status) {
    filtered = filtered.filter(
      (row) => row.statusKerja === appliedFilterData.value.status,
    );
  }

  // Filter berdasarkan hasil (checkbox) - hanya jika ada filter yang diterapkan
  const hasAnyFilterSelected =
    appliedFilterHasil.value.normal ||
    appliedFilterHasil.value.abnormal ||
    appliedFilterHasil.value.warning;
  if (hasAnyFilterSelected) {
    filtered = filtered.filter((row) => {
      if (row.hasil === "Normal" && appliedFilterHasil.value.normal)
        return true;
      if (row.hasil === "Abnormal" && appliedFilterHasil.value.abnormal)
        return true;
      if (row.hasil === "Warning" && appliedFilterHasil.value.warning)
        return true;
      return false;
    });
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

const openFilter = () => {
  showFilter.value = true;
};

const closeFilter = () => {
  showFilter.value = false;
};

const applyFilter = () => {
  appliedFilterHasil.value = { ...filterHasil.value };
  appliedFilterDate.value = { ...filterDate.value };
  appliedFilterData.value = { ...filterData.value };
  currentPage.value = 1;
  closeFilter();
};

// Export filters computed property
const exportFilters = computed(() => {
  const filters = {
    kategori: "IMM",
  };

  if (searchQuery.value) {
    filters.search = searchQuery.value;
  }

  // Add status filter - backend expects single report_status value
  // If multiple selected, use the first one
  if (appliedFilterHasil.value.normal) {
    filters.report_status = "normal";
  } else if (appliedFilterHasil.value.abnormal) {
    filters.report_status = "abnormal";
  } else if (appliedFilterHasil.value.warning) {
    filters.report_status = "warning";
  }

  return filters;
});

// Function untuk menghapus data yang dipilih
const handleDeleteSelected = async () => {
  if (selectedRowIds.value.length === 0) {
    alert("Tidak ada data yang dipilih untuk dihapus");
    return;
  }

  const confirmDelete = confirm(
    `Apakah Anda yakin ingin menghapus ${selectedRowIds.value.length} data P2H yang dipilih?\n\nData akan di-soft delete dan dapat dipulihkan oleh administrator.`,
  );

  if (!confirmDelete) {
    return;
  }

  try {
    isLoading.value = true;
    console.log(
      "🗑️ [PT] Menghapus data P2H (soft delete):",
      selectedRowIds.value,
    );

    // Delete each selected report
    const deletePromises = selectedRowIds.value.map(async (reportId) => {
      try {
        await api.delete(`/p2h/reports/${reportId}`);
        console.log(`✅ Berhasil menghapus report ${reportId}`);
        return { success: true, id: reportId };
      } catch (error) {
        console.error(`❌ Gagal menghapus report ${reportId}:`, error);
        return { success: false, id: reportId, error };
      }
    });

    const results = await Promise.all(deletePromises);
    const successCount = results.filter((r) => r.success).length;
    const failCount = results.filter((r) => !r.success).length;

    if (successCount > 0) {
      alert(
        `Berhasil menghapus ${successCount} data P2H${failCount > 0 ? `. ${failCount} data gagal dihapus.` : ""}`,
      );

      // Refresh data
      await fetchP2HReports();

      // Clear selection
      selectedRowIds.value = [];
      selectAllChecked.value = false;
    } else {
      alert("Gagal menghapus data P2H. Silakan coba lagi.");
    }
  } catch (error) {
    console.error("❌ Error saat menghapus data:", error);
    alert(
      "Terjadi kesalahan saat menghapus data: " +
        (error.message || "Unknown error"),
    );
  } finally {
    isLoading.value = false;
  }
};

// Load data saat component mounted
onMounted(() => {
  fetchP2HReports();
});
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
          <!-- Judul - Sticky -->
          <div class="mb-2 shrink-0 sticky top-0 z-30 bg-[#EFEFEF]">
            <div class="bg-white rounded-lg shadow-md p-1 pl-5">
              <h1 class="text-base font-bold text-[#523E95] text-left">
                PT Indominco Mandiri
              </h1>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow-md p-5 flex flex-col">
            <!-- Toolbar - Sticky inside card -->
            <div
              class="flex flex-wrap items-center gap-2 md:gap-3 pb-4 border-b shrink-0 flex-none top-14 bg-white"
            >
              <!-- Search Input with Icon Inside -->
              <div class="relative flex w-full md:w-auto md:min-w-56 order-1">
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

              <!-- Filter Button -->
              <button
                @click="openFilter"
                class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition text-sm order-2"
              >
                <Bars3BottomLeftIcon class="w-4 h-4" />
                <span class="hidden sm:inline">Filter</span>
              </button>

              <!-- Export Dropdown -->
              <div class="order-3">
                <ExportDropdown
                  export-endpoint="/export/p2h-reports"
                  :filters="exportFilters"
                />
              </div>

              <!-- Delete Button -->
              <button
                @click="handleDeleteSelected"
                :disabled="selectedRowIds.length === 0"
                class="flex items-center gap-2 px-3 py-2 rounded-md transition text-sm order-4"
                :class="
                  selectedRowIds.length > 0
                    ? 'bg-red-100 text-red-700 border border-red-300 hover:bg-red-200'
                    : 'bg-gray-100 text-gray-400 border border-gray-300 cursor-not-allowed'
                "
              >
                <TrashIcon class="w-4 h-4" />
                <span class="hidden sm:inline">Hapus</span>
              </button>
            </div>

            <!-- Table Container with Horizontal Scroll -->
            <div
              class="flex flex-col gap-4 bg-gray-50 p-1 rounded-lg border border-gray-200 mt-4"
            >
              <!-- Loading state -->
              <div
                v-if="isLoading"
                class="flex justify-center items-center py-12 bg-white rounded-lg border"
              >
                <div
                  class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"
                ></div>
                <span class="ml-3 text-gray-600">Memuat data...</span>
              </div>

              <!-- Empty state -->
              <div
                v-else-if="tableData.length === 0"
                class="flex justify-center items-center py-12 bg-white rounded-lg border"
              >
                <p class="text-gray-500 text-lg">Belum ada data P2H</p>
              </div>

              <!-- Table with data -->
              <div
                v-else
                class="overflow-x-auto overflow-y-auto rounded-lg border bg-white max-h-150"
              >
                <table class="w-full border-collapse">
                  <thead class="sticky top-0 z-10">
                    <tr class="border-b-2 border-gray-400 bg-gray-50">
                      <th
                        class="px-2 md:px-3 py-3 text-center font-semibold text-gray-700 whitespace-nowrap w-10 md:w-12"
                      >
                        <div class="flex items-center justify-center">
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
                            <!-- Check Icon -->
                            <CheckIcon
                              v-if="selectAllChecked"
                              class="absolute inset-0 m-auto w-4 h-4 text-white pointer-events-none"
                            />
                          </div>
                        </div>
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-32"
                      >
                        Tanggal / Waktu
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-24"
                      >
                        No. Lambung
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Nomor Polisi
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-20"
                      >
                        Tipe
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-20"
                      >
                        Merek
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Nama Pemeriksa
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-20"
                      >
                        Shift
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Kategori Layanan
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Perusahaan
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-20"
                      >
                        Hasil
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-40"
                      >
                        Keterangan
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
                        class="px-2 md:px-3 py-3 text-center whitespace-nowrap w-10 md:w-12"
                      >
                        <div class="flex items-center justify-center">
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

                            <!-- Check Icon -->
                            <CheckIcon
                              v-if="isRowSelected(row.id)"
                              class="absolute inset-0 m-auto w-4 h-4 text-white pointer-events-none"
                            />
                          </div>
                        </div>
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 whitespace-nowrap min-w-32"
                      >
                        <div class="text-xs">{{ row.tanggal }}</div>
                        <div class="text-xs text-gray-600">{{ row.waktu }}</div>
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-24"
                      >
                        {{ row.noLambung }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.nomorPolisi }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-20"
                      >
                        {{ row.tipe }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-20"
                      >
                        {{ row.merek }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.namaPemeriksa }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-20"
                      >
                        {{ row.shift }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.kategoriLayanan }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.perusahaan }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-20"
                      >
                        <span
                          class="px-3 py-1 rounded-full text-sm font-semibold"
                          :style="{
                            backgroundColor: getResultColor(row.hasil).bg,
                            color: getResultColor(row.hasil).text,
                          }"
                        >
                          {{ row.hasil }}
                        </span>
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs min-w-40"
                        :class="
                          row.hasKeterangan
                            ? 'text-red-600 font-medium'
                            : 'text-gray-400'
                        "
                      >
                        <div v-if="row.hasKeterangan" class="space-y-2">
                          <div
                            v-for="(
                              notes, category
                            ) in row.keteranganByCategory"
                            :key="category"
                          >
                            <div
                              class="font-semibold text-xs mb-1 text-gray-700"
                            >
                              {{ category }}:
                            </div>
                            <ul class="list-disc list-inside space-y-1 ml-2">
                              <li
                                v-for="(ket, idx) in notes"
                                :key="idx"
                                class="text-xs"
                              >
                                {{ ket }}
                              </li>
                            </ul>
                          </div>
                        </div>
                        <span v-else class="text-gray-400">-</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Pagination -->
              <div
                v-if="tableData.length > 0"
                class="flex flex-col md:flex-row justify-between items-center gap-3 md:gap-4 pt-3 md:pt-4 border-t border-gray-200"
              >
                <!-- Items per page selector -->
                <div class="flex items-center gap-2 order-1 md:order-1">
                  <label class="text-xs md:text-sm text-gray-700 font-medium"
                    >Tampilkan</label
                  >
                  <select
                    v-model="itemsPerPage"
                    @change="currentPage = 1"
                    class="px-2 md:px-3 py-1 md:py-1.5 border border-gray-300 rounded-md text-xs md:text-sm text-gray-700 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                  >
                    <option :value="10">10</option>
                    <option :value="20">20</option>
                    <option :value="50">50</option>
                    <option :value="100">100</option>
                  </select>
                  <span class="text-xs md:text-sm text-gray-700 font-medium"
                    >baris</span
                  >
                </div>

                <!-- Navigation and info -->
                <div class="flex items-center gap-3 order-2 md:order-2">
                  <button
                    @click="previousPage"
                    :disabled="currentPage === 1"
                    class="px-2 md:px-3 py-1 md:py-2 border border-gray-300 rounded-md text-gray-700 font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition"
                  >
                    &lt;
                  </button>

                  <span class="text-xs md:text-sm text-gray-700 font-medium">
                    {{ startIndex }} - {{ endIndex }} dari
                    {{ filteredTableData.length }}
                  </span>

                  <button
                    @click="nextPage"
                    :disabled="currentPage === totalPages"
                    class="px-2 md:px-3 py-1 md:py-2 border border-gray-300 rounded-md text-gray-700 font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition"
                  >
                    &gt;
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Filter Konten -->
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

              <!-- Filter Date -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Start Date</label
                  >
                  <div class="relative">
                    <input
                      v-model="filterDate.start"
                      type="date"
                      placeholder="hh / bb / tttt"
                      class="w-full p-2 text-xs border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                    />
                  </div>
                </div>
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >End Date</label
                  >
                  <div class="relative">
                    <input
                      v-model="filterDate.end"
                      type="date"
                      placeholder="hh / bb / tttt"
                      class="w-full p-2 text-xs border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                    />
                  </div>
                </div>
              </div>

              <!-- Filter Hasil -->
              <div>
                <label class="block text-sm font-medium text-black mb-2 mt-4"
                  >Hasil</label
                >
                <div class="flex gap-4">
                  <div class="flex items-center">
                    <input
                      v-model="filterHasil.normal"
                      type="checkbox"
                      id="normal"
                      class="w-4 h-4 cursor-pointer rounded border-2 border-gray-300"
                      style="
                        appearance: none;
                        -webkit-appearance: none;
                        -moz-appearance: none;
                      "
                      :style="
                        filterHasil.normal
                          ? {
                              backgroundColor: '#A7E8BF',
                              borderColor: '#1A5C3F',
                            }
                          : { backgroundColor: 'white', borderColor: '#d1d5db' }
                      "
                    />
                    <label
                      for="normal"
                      class="ml-2 text-sm text-black cursor-pointer"
                      >Normal</label
                    >
                  </div>
                  <div class="flex items-center">
                    <input
                      v-model="filterHasil.abnormal"
                      type="checkbox"
                      id="abnormal"
                      class="w-4 h-4 cursor-pointer rounded border-2 border-gray-300"
                      style="
                        appearance: none;
                        -webkit-appearance: none;
                        -moz-appearance: none;
                      "
                      :style="
                        filterHasil.abnormal
                          ? {
                              backgroundColor: '#F7E19C',
                              borderColor: '#8B6F47',
                            }
                          : { backgroundColor: 'white', borderColor: '#d1d5db' }
                      "
                    />
                    <label
                      for="abnormal"
                      class="ml-2 text-sm text-black cursor-pointer"
                      >Abnormal</label
                    >
                  </div>
                  <div class="flex items-center">
                    <input
                      v-model="filterHasil.warning"
                      type="checkbox"
                      id="warning"
                      class="w-4 h-4 cursor-pointer rounded border-2 border-gray-300"
                      style="
                        appearance: none;
                        -webkit-appearance: none;
                        -moz-appearance: none;
                      "
                      :style="
                        filterHasil.warning
                          ? {
                              backgroundColor: '#FFA0A0',
                              borderColor: '#8B3A3A',
                            }
                          : { backgroundColor: 'white', borderColor: '#d1d5db' }
                      "
                    />
                    <label
                      for="warning"
                      class="ml-2 text-sm text-black cursor-pointer"
                      >Warning</label
                    >
                  </div>
                </div>
              </div>

              <!-- Perusahaan -->
              <div>
                <label class="block text-sm font-medium text-gray-800 mb-2 mt-2"
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
                <label class="block text-sm font-medium text-gray-800 mb-2 mt-2"
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

              <!-- Departemen -->
              <div>
                <label class="block text-sm font-medium text-gray-800 mb-2 mt-2"
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
                <label class="block text-sm font-medium text-gray-800 mb-2 mt-2"
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
        </main>
      </div>
    </div>
  </div>
</template>
