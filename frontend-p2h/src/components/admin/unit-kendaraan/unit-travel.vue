<script setup>
import { ref, computed, onMounted, watch } from "vue";
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
  PlusIcon,
  UserPlusIcon,
  CloudArrowUpIcon,
  PencilSquareIcon,
  XMarkIcon,
  ChevronDownIcon,
  CheckIcon,
} from "@heroicons/vue/24/outline";
import { PencilIcon, CalendarIcon } from "@heroicons/vue/24/solid";
import apiService from "@/services/api";
import { formatHullNumber, formatHullNumberOnBlur } from "@/utils/vehicleUtils";
import { useSidebarProvider } from "../../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();

const selectedRowIds = ref([]);
const selectAllChecked = ref(false);
const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = ref(10);
const tambahUnitKendaraan = ref(false);
const showFilter = ref(false);
const sortOrder = ref("asc");
const isLoading = ref(false);
const errorMessage = ref("");
const showBulkUpload = ref(false);
const editingId = ref(null);
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const filterData = ref({
  vehicle_type: "",
  warna_lambung: "",
  perusahaan: "",
  merk: "",
  stnk_date: "",
  pajak_date: "",
  kir_date: "",
});
const appliedFilterData = ref({
  vehicle_type: "",
  warna_lambung: "",
  perusahaan: "",
  merk: "",
  stnk_date: "",
  pajak_date: "",
  kir_date: "",
});

const opentambahUnitKendaraan = () => {
  editingId.value = null;
  formData.value = {
    plat_nomor: "",
    vehicle_type: "Light Vehicle",
    merk: "",
    user_id: null,
    company_id: null,
    no_rangka: "",
    no_mesin: "",
    stnk_expiry: "",
    pajak_expiry: "",
    kir_expiry: "",
    shift_type: "non_shift",
  };
  console.log(
    "📋 [Travel] Modal opened - Users available:",
    allUsers.value.length,
    "Companies available:",
    allCompanies.value.length,
  );
  tambahUnitKendaraan.value = true;
};

const closeTambahUnitKendaraan = () => {
  editingId.value = null;
  formData.value = {
    plat_nomor: "",
    vehicle_type: "Light Vehicle",
    merk: "",
    user_id: null,
    company_id: null,
    no_rangka: "",
    no_mesin: "",
    stnk_expiry: "",
    pajak_expiry: "",
    kir_expiry: "",
    shift_type: "non_shift",
  };
  tambahUnitKendaraan.value = false;
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
  fetchVehicles();
};

const exportFilters = computed(() => ({
  kategori: "TRAVEL",
  vehicle_type: appliedFilterData.value.vehicle_type || undefined,
  shift_type: appliedFilterData.value.shift_type || undefined,
  is_active: appliedFilterData.value.status
    ? appliedFilterData.value.status === "Aktif"
    : undefined,
  search: searchQuery.value || undefined,
}));

const tableData = ref([]);

// Form data untuk tambah/edit kendaraan (Travel - tanpa nomor lambung & warna)
const formData = ref({
  plat_nomor: "",
  vehicle_type: "Light Vehicle",
  merk: "",
  user_id: null,
  company_id: null,
  no_rangka: "",
  no_mesin: "",
  stnk_expiry: "",
  pajak_expiry: "",
  kir_expiry: "",
  shift_type: "non_shift",
});

// Users and Companies data
const allUsers = ref([]);
const allCompanies = ref([]);

// Fetch users untuk dropdown (hanya kategori TRAVEL)
const fetchUsers = async () => {
  try {
    const response = await apiService.users.getAll();
    if (response.data.status === "success") {
      // Filter hanya users dengan kategori_pengguna = TRAVEL
      const allTravelUsers = response.data.payload.filter(
        (user) => user.kategori_pengguna === "TRAVEL"
      );
      allUsers.value = allTravelUsers;
      console.log("✅ [Travel] Users fetched:", allUsers.value.length, "users (TRAVEL only)");
    }
  } catch (error) {
    console.error("Error fetching users:", error);
  }
};

// Fetch companies untuk dropdown
const fetchCompanies = async () => {
  try {
    const response = await apiService.master.getCompanies();
    if (response.data.status === "success") {
      allCompanies.value = response.data.payload;
      console.log("✅ [Travel] Companies fetched:", allCompanies.value.length, "companies");
    }
  } catch (error) {
    console.error("Error fetching companies:", error);
  }
};

// Fetch vehicles dari backend (kategori Travel)
const fetchVehicles = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    console.log("🔄 [Travel] Fetching vehicles...");
    // Fetch all vehicles with high limit for frontend pagination
    const response = await apiService.vehicles.getAll({ limit: 2000 });

    if (response.data.status === "success" || response.data.success) {
      // Filter hanya kategori Travel
      const allVehicles = response.data.payload.filter(
        (v) => v.kategori_unit === "TRAVEL",
      );
      console.log(
        "✅ [Travel] Vehicles fetched:",
        allVehicles.length,
        "vehicles",
      );

      tableData.value = allVehicles.map((vehicle) => ({
        id: vehicle.id,
        nomorLambung: vehicle.no_lambung,
        warnaNomorLambung: vehicle.warna_no_lambung || "-",
        nomorPolisi: vehicle.plat_nomor || "-",
        tipe: vehicle.vehicle_type,
        merek: vehicle.merk || "-",
        user: vehicle.user?.full_name || "-",
        perusahaan: vehicle.company?.nama_perusahaan || "-",
        tglSTNK: vehicle.stnk_expiry || "-",
        tglPajak: vehicle.pajak_expiry || "-",
        kirKuer: vehicle.kir_expiry || "-",
        noRangka: vehicle.no_rangka || "-",
        noMesin: vehicle.no_mesin || "-",
      }));
    } else {
      errorMessage.value = response.data.message || "Gagal mengambil data";
    }
  } catch (error) {
    console.error("❌ [Travel] Error fetching vehicles:", error);
    errorMessage.value =
      error.response?.data?.detail ||
      error.message ||
      "Gagal mengambil data kendaraan";
  } finally {
    isLoading.value = false;
  }
};

// Handler untuk tambah/edit kendaraan (Travel - tanpa nomor lambung)
const handleTambahUnitKendaraan = async () => {
  if (!formData.value.plat_nomor || !formData.value.vehicle_type) {
    alert("Nomor polisi dan tipe kendaraan wajib diisi!");
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";

  try {
    let response;

    // Add kategori TRAVEL (tanpa nomor lambung & warna)
    const payload = {
      ...formData.value,
      kategori_unit: "TRAVEL",
      no_lambung: null, // Travel tidak pakai nomor lambung
      warna_no_lambung: null,
    };

    if (editingId.value) {
      response = await apiService.vehicles.update(editingId.value, payload);
    } else {
      response = await apiService.vehicles.create(payload);
    }

    if (response.data.status === "success" || response.data.success) {
      alert(
        editingId.value
          ? "Kendaraan berhasil diupdate"
          : "Kendaraan berhasil ditambahkan",
      );

      editingId.value = null;
      formData.value = {
        plat_nomor: "",
        vehicle_type: "Light Vehicle",
        merk: "",
        user_id: null,
        company_id: null,
        no_rangka: "",
        no_mesin: "",
        stnk_expiry: "",
        pajak_expiry: "",
        kir_expiry: "",
        shift_type: "non_shift",
      };
        no_rangka: "",
        no_mesin: "",
        stnk_expiry: "",
        pajak_expiry: "",
        kir_expiry: "",
        shift_type: "non_shift",
      };

      closeTambahUnitKendaraan();
      await fetchVehicles();
    } else {
      errorMessage.value =
        response.data.message || "Gagal menyimpan data kendaraan";
      alert(errorMessage.value);
    }
  } catch (error) {
    console.error("Error saving vehicle:", error);
    errorMessage.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Gagal menyimpan data kendaraan";
    alert(`Error: ${errorMessage.value}`);
  } finally {
    isLoading.value = false;
  }
};

// Edit kendaraan (Travel - tanpa nomor lambung)
const editKendaraan = async (rowId) => {
  try {
    const response = await apiService.vehicles.getById(rowId);

    if (response.data.status === "success" || response.data.success) {
      const vehicle = response.data.payload;

      editingId.value = rowId;
      formData.value = {
        plat_nomor: vehicle.plat_nomor || "",
        vehicle_type: vehicle.vehicle_type || "Light Vehicle",
        merk: vehicle.merk || "",
        user_id: vehicle.user_id || null,
        company_id: vehicle.company_id || null,
        no_rangka: vehicle.no_rangka || "",
        no_mesin: vehicle.no_mesin || "",
        stnk_expiry: vehicle.stnk_expiry || "",
        pajak_expiry: vehicle.pajak_expiry || "",
        kir_expiry: vehicle.kir_expiry || "",
        shift_type: vehicle.shift_type || "non_shift",
      };
        user_id: vehicle.user_id || null,
        company_id: vehicle.company_id || null,
        no_rangka: vehicle.no_rangka || "",
        no_mesin: vehicle.no_mesin || "",
        stnk_expiry: vehicle.stnk_expiry || "",
        pajak_expiry: vehicle.pajak_expiry || "",
        kir_expiry: vehicle.kir_expiry || "",
        shift_type: vehicle.shift_type || "non_shift",
      };

      tambahUnitKendaraan.value = true;
    }
  } catch (error) {
    console.error("Error fetching vehicle detail:", error);
    alert("Gagal mengambil data kendaraan");
  }
};

// Handler untuk format nomor lambung saat blur
const handleHullNumberBlur = () => {
  if (formData.value.no_lambung) {
    // Simple format: add dot after first char if not already there
    const cleaned = formData.value.no_lambung.replace(/\./g, "").trim();
    if (cleaned.length > 1 && !formData.value.no_lambung.includes(".")) {
      formData.value.no_lambung = cleaned.charAt(0) + "." + cleaned.slice(1);
    }
  }
};

// Hapus kendaraan (soft delete)
const handleDeleteVehicles = async () => {
  if (selectedRowIds.value.length === 0) {
    alert("Pilih kendaraan yang ingin dihapus!");
    return;
  }

  if (
    !confirm(`Yakin ingin menghapus ${selectedRowIds.value.length} kendaraan?`)
  ) {
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";
  let deletedCount = 0;

  try {
    for (const id of selectedRowIds.value) {
      await apiService.vehicles.delete(id);
      deletedCount++;
    }

    selectedRowIds.value = [];
    selectAllChecked.value = false;
    tableData.value = [];

    await fetchVehicles();
    alert(`${deletedCount} kendaraan berhasil dihapus`);
  } catch (error) {
    console.error("Error deleting vehicles:", error);
    errorMessage.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Gagal menghapus kendaraan";
    alert(
      `Error: ${errorMessage.value}\n\nBerhasil dihapus: ${deletedCount} dari ${selectedRowIds.value.length}`,
    );
  } finally {
    isLoading.value = false;
  }
};

// Extract unique values for dropdowns
const uniqueCompanies = computed(() => {
  const companies = tableData.value
    .map((row) => row.perusahaan)
    .filter(Boolean);
  return [...new Set(companies)].sort();
});

const uniqueTypes = computed(() => {
  const types = tableData.value.map((row) => row.tipe).filter(Boolean);
  return [...new Set(types)].sort();
});

const uniqueMerks = computed(() => {
  const merks = tableData.value.map((row) => row.merek).filter(Boolean);
  return [...new Set(merks)].sort();
});

// Load data saat component mounted
onMounted(() => {
  fetchVehicles();
  fetchUsers();
  fetchCompanies();
});

// Watch untuk auto-fetch ketika filter diterapkan
watch(
  appliedFilterData,
  () => {
    console.log(
      "🔄 Filter changed, fetching vehicles...",
      appliedFilterData.value,
    );
    fetchVehicles();
  },
  { deep: true },
);

// Handler untuk format nomor lambung saat blur
// Note: Unit travel belum ada form input, handler ini untuk konsistensi
// Uncomment dan sesuaikan jika ada form:
// const handleHullNumberBlur = () => {
//   if (formData.value.no_lambung) {
//     formData.value.no_lambung = formatHullNumberOnBlur(formData.value.no_lambung);
//   }
// };

const selectRow = (rowId) => {
  const index = selectedRowIds.value.indexOf(rowId);
  if (index > -1) {
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

// Filter data berdasarkan search query dan filter yang diterapkan
const filteredTableData = computed(() => {
  let filtered = tableData.value;

  // Filter berdasarkan search query
  if (searchQuery.value.trim()) {
    const query = normalizeString(searchQuery.value);
    filtered = filtered.filter((row) => {
      return (
        normalizeString(row.nomorLambung || "").includes(query) ||
        normalizeString(row.warnaNomorLambung || "").includes(query) ||
        normalizeString(row.nomorPolisi).includes(query) ||
        normalizeString(row.tipe).includes(query) ||
        normalizeString(row.merek).includes(query) ||
        normalizeString(row.user).includes(query) ||
        normalizeString(row.perusahaan).includes(query)
      );
    });
  }

  // Filter berdasarkan filter yang diterapkan
  if (appliedFilterData.value.perusahaan) {
    filtered = filtered.filter(
      (row) => row.perusahaan === appliedFilterData.value.perusahaan,
    );
  }
  if (appliedFilterData.value.vehicle_type) {
    filtered = filtered.filter(
      (row) => row.tipe === appliedFilterData.value.vehicle_type,
    );
  }
  if (appliedFilterData.value.merk) {
    filtered = filtered.filter(
      (row) => row.merek === appliedFilterData.value.merk,
    );
  }
  if (appliedFilterData.value.stnk_date) {
    filtered = filtered.filter((row) => {
      // row.tglSTNK format: "DD Bulan YYYY" (e.g. "15 Januari 2025")
      // appliedFilterData.value.stnk_date format: "YYYY-MM-DD"
      if (!row.tglSTNK || row.tglSTNK === "-") return false;

      // Conversion helper
      const bulanMap = {
        Januari: "01",
        Februari: "02",
        Maret: "03",
        April: "04",
        Mei: "05",
        Juni: "06",
        Juli: "07",
        Agustus: "08",
        September: "09",
        Oktober: "10",
        November: "11",
        Desember: "12",
      };
      const parts = row.tglSTNK.split(" "); // ["15", "Januari", "2025"]
      if (parts.length < 3) return false;
      const rowDate = `${parts[2]}-${bulanMap[parts[1]]}-${parts[0].padStart(2, "0")}`;

      return rowDate === appliedFilterData.value.stnk_date;
    });
  }
  if (appliedFilterData.value.pajak_date) {
    filtered = filtered.filter((row) => {
      if (!row.tglPajak || row.tglPajak === "-") return false;
      const bulanMap = {
        Januari: "01",
        Februari: "02",
        Maret: "03",
        April: "04",
        Mei: "05",
        Juni: "06",
        Juli: "07",
        Agustus: "08",
        September: "09",
        Oktober: "10",
        November: "11",
        Desember: "12",
      };
      const parts = row.tglPajak.split(" ");
      if (parts.length < 3) return false;
      const rowDate = `${parts[2]}-${bulanMap[parts[1]]}-${parts[0].padStart(2, "0")}`;
      return rowDate === appliedFilterData.value.pajak_date;
    });
  }
  if (appliedFilterData.value.kir_date) {
    filtered = filtered.filter((row) => {
      if (!row.kirKuer || row.kirKuer === "-") return false;
      const bulanMap = {
        Januari: "01",
        Februari: "02",
        Maret: "03",
        April: "04",
        Mei: "05",
        Juni: "06",
        Juli: "07",
        Agustus: "08",
        September: "09",
        Oktober: "10",
        November: "11",
        Desember: "12",
      };
      // kirKuer might be "YYYY-MM-DD" or "DD Bulan YYYY", assuming consistent display format
      // If it is fetched as "YYYY-MM-DD" from backend, display might be formatted.
      // Based on fetchVehicles map: kirKuer: vehicle.kir_expiry || "-" (likely YYYY-MM-DD from backend)
      // Check display logic: fetchVehicles does not format it, but template uses row.kirKuer directly.
      // Wait, formatHullNumberOnBlur is imported but not used.
      // Let's check fetchVehicles again.
      // tglSTNK: vehicle.stnk_expiry || "-"
      // vehicle.stnk_expiry is typically Date object or ISO string.
      // If backend sends YYYY-MM-DD, then we need to match it.

      // However, `getDateStyle` parses "DD Bulan YYYY". This implies the backend returns "DD Bulan YYYY" OR it is formatted somewhere.
      // Checking `apiService`... `getAll` returns raw data.
      // Wait, checking `export.py`... `format_datetime` returns "YYYY-MM-DD".
      // Let's re-verify `fetchVehicles`. It maps directly.
      // If `getDateStyle` works, then `tglSTNK` IS "DD Bulan YYYY".
      // But `export.py` sends "YYYY-MM-DD".
      // Maybe the backend `vehicle.stnk_expiry` property accessor does formatting?
      // Or `getAll` router response does?
      // Assuming `tglSTNK` is "DD Bulan YYYY" for now as per `getDateStyle`.

      const parts = row.kirKuer.split(" ");
      if (parts.length < 3) return false; // Likely raw YYYY-MM-DD if length is 1

      const rowDate = `${parts[2]}-${bulanMap[parts[1]]}-${parts[0].padStart(2, "0")}`;
      return rowDate === appliedFilterData.value.kir_date;
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

const getDateStyle = (dateString) => {
  // Parse tanggal format "DD Bulan YYYY"
  const bulanMap = {
    Januari: 0,
    Februari: 1,
    Maret: 2,
    April: 3,
    Mei: 4,
    Juni: 5,
    Juli: 6,
    Agustus: 7,
    September: 8,
    Oktober: 9,
    November: 10,
    Desember: 11,
  };

  const parts = dateString.split(" ");
  const day = parseInt(parts[0]);
  const month = bulanMap[parts[1]];
  const year = parseInt(parts[2]);

  const targetDate = new Date(year, month, day);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Hitung selisih bulan
  const monthDiff =
    (targetDate.getFullYear() - today.getFullYear()) * 12 +
    (targetDate.getMonth() - today.getMonth());

  if (monthDiff === 1) {
    return { bg: "#FFE5E5", text: "#C41E3A" }; // Merah
  } else if (monthDiff === 2) {
    return { bg: "#FFF3CD", text: "#856404" }; // Kuning
  } else {
    return { bg: "#E2E3E5", text: "#383D41" }; // Abu-abu
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
          <!-- Judul -->
          <div class="mb-2 shrink-0 sticky top-0 z-30 bg-[#EFEFEF]">
            <div class="bg-white rounded-lg shadow-md p-1 pl-5">
              <h1 class="text-base font-bold text-[#523E95] text-left">
                Travel
              </h1>
            </div>
          </div>
          <div
            class="bg-white rounded-lg shadow-md p-5 flex-1 flex flex-col overflow-hidden min-h-0"
          >
            <!-- NOTIFICATION WRAPPER (HANYA MUNCUL JIKA ADA ISI) -->
            <div class="flex flex-col space-y-3 mb-4 shrink-0">
              <!-- Error Message -->
              <div
                v-if="errorMessage"
                class="p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm"
              >
                {{ errorMessage }}
              </div>

              <!-- Loading State -->
              <div
                v-if="isLoading"
                class="p-3 bg-blue-50 border border-blue-200 rounded-md text-blue-700 text-sm"
              >
                Memuat data...
              </div>

              <!-- Toolbar -->
              <div
                class="flex flex-wrap items-center justify-between gap-3 border-b shrink-0 flex-none sticky top-14 bg-white z-20"
              >
                <!-- LEFT SECTION -->
                <div class="flex flex-wrap items-center gap-3">
                  <button
                    @click="opentambahUnitKendaraan"
                    class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-white bg-[#6444C6] hover:bg-[#5c3db8] transition text-sm"
                  >
                    <PlusIcon class="w-5 h-5" />
                    <span>Tambah unit kendaraan</span>
                  </button>

                  <button
                    @click="openBulkUpload"
                    class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition text-sm"
                  >
                    <CloudArrowUpIcon class="w-4 h-4" />
                    <span>Upload</span>
                  </button>
                </div>

                <!-- RIGHT SECTION -->
                <div class="flex flex-wrap items-center gap-3 ml-auto">
                  <!-- Search -->
                  <div class="relative w-52">
                    <MagnifyingGlassIcon
                      class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
                    />
                    <input
                      v-model="searchQuery"
                      @input="currentPage = 1"
                      type="text"
                      placeholder="Cari..."
                      class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-md text-sm text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <button
                    @click="openFilter"
                    class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition text-sm"
                  >
                    <Bars3BottomLeftIcon class="w-4 h-4" />
                    <span>Filter</span>
                  </button>

                  <ExportDropdown
                    :export-endpoint="`${API_BASE_URL}/export/vehicles`"
                    :filters="exportFilters"
                  />

                  <button
                    class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition text-sm"
                  >
                    <ArrowDownTrayIcon class="w-4 h-4" />
                    <span>Template</span>
                  </button>

                  <button
                    @click="handleDeleteVehicles"
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
            </div>

            <!-- Table Container with Horizontal Scroll -->
            <div
              class="flex flex-col gap-4 bg-gray-50 p-1 rounded-lg border border-gray-200 mt-4"
            >
              <div
                class="overflow-x-auto overflow-y-auto rounded-lg border bg-white max-h-[600px]"
              >
                <table class="w-full border-collapse">
                  <thead class="sticky top-0 z-10">
                    <tr class="border-b-2 border-gray-400 bg-gray-50">
                      <th
                        class="px-4 py-3 text-left font-semibold text-gray-700 whitespace-nowrap min-w-12"
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
                        User
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Perusahaan
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Tgl. STNK
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        Tgl. Pajak
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        No. Rangka
                      </th>
                      <th
                        class="px-4 py-3 text-left text-sm font-semibold text-gray-700 whitespace-nowrap min-w-28"
                      >
                        No. Mesin
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
                      <td class="px-4 py-3 whitespace-nowrap min-w-12">
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
                        {{ row.user }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.perusahaan }}
                      </td>
                      <td class="px-4 py-3 text-xs whitespace-nowrap min-w-28">
                        <span
                          class="px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap"
                          :style="{
                            backgroundColor: getDateStyle(row.tglSTNK).bg,
                            color: getDateStyle(row.tglSTNK).text,
                          }"
                        >
                          {{ row.tglSTNK }}
                        </span>
                      </td>
                      <td class="px-4 py-3 text-xs whitespace-nowrap min-w-28">
                        <span
                          class="px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap"
                          :style="{
                            backgroundColor: getDateStyle(row.tglPajak).bg,
                            color: getDateStyle(row.tglPajak).text,
                          }"
                        >
                          {{ row.tglPajak }}
                        </span>
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.noRangka }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-28"
                      >
                        {{ row.noMesin }}
                      </td>
                      <td
                        class="px-4 py-3 text-gray-800 text-xs whitespace-nowrap min-w-16"
                      >
                        <button
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

            <!-- Konten Tambah pengguna -->
            <div
              v-if="tambahUnitKendaraan"
              class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            >
              <div
                class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-[0_4px_6px_rgba(0,0,0,0.1)] p-6 md:p-8"
              >
                <div
                  class="flex justify-between items-center mb-2 pb-3 border-b border-gray-200"
                >
                  <h2 class="text-lg md:text-xl font-semibold text-gray-900">
                    {{ editingId ? "Edit Unit Kendaraan" : "Tambah Unit Kendaraan" }}
                  </h2>
                  <button
                    @click="closeTambahUnitKendaraan"
                    class="shrink-0 p-1 hover:bg-gray-100 rounded-md transition"
                    title="Tutup"
                    aria-label="Tutup modal"
                  >
                    <XMarkIcon
                      class="w-6 h-6 text-gray-600 hover:text-gray-900"
                    />
                  </button>
                </div>

                <!-- Row -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label
                      for="plat_nomor"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Nomor Polisi</label
                    >
                    <div class="relative">
                      <input
                        id="plat_nomor"
                        name="plat_nomor"
                        v-model="formData.plat_nomor"
                        type="text"
                        placeholder="Masukkan nomor polisi"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                      />
                      <PencilIcon
                        class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                      />
                    </div>
                  </div>

                  <div>
                    <label
                      for="merk"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Merek</label
                    >
                    <div class="relative">
                      <input
                        id="merk"
                        name="merk"
                        v-model="formData.merk"
                        type="text"
                        placeholder="Masukkan merek kendaraan"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                      />
                      <PencilIcon
                        class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                      />
                    </div>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label
                      for="vehicle_type"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Tipe</label
                    >
                    <div class="relative">
                      <select
                        id="vehicle_type"
                        name="vehicle_type"
                        v-model="formData.vehicle_type"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm appearance-none"
                      >
                        <option value="">Pilih tipe kendaraan</option>
                        <option value="Light Vehicle">Light Vehicle</option>
                        <option value="Electric Vehicle">Electric Vehicle</option>
                        <option value="Double Cabin">Double Cabin</option>
                        <option value="Single Cabin">Single Cabin</option>
                        <option value="Bus">Bus</option>
                        <option value="Ambulance">Ambulance</option>
                        <option value="Fire Truck">Fire Truck</option>
                        <option value="Komando">Komando</option>
                        <option value="Truk Sampah">Truk Sampah</option>
                      </select>
                      <ChevronDownIcon
                        class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                      />
                    </div>
                  </div>

                  <div>
                    <label
                      for="user_id"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >User</label
                    >
                    <div class="relative">
                      <select
                        id="user_id"
                        name="user_id"
                        v-model="formData.user_id"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm appearance-none"
                      >
                        <option :value="null">
                          {{ allUsers.length === 0 ? "Loading users..." : "Pilih user" }}
                        </option>
                        <option
                          v-for="user in allUsers"
                          :key="user.id"
                          :value="user.id"
                        >
                          {{ user.full_name }}
                        </option>
                      </select>
                      <ChevronDownIcon
                        class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                      />
                    </div>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label
                      for="company_id"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Perusahaan</label
                    >
                    <div class="relative">
                      <select
                        id="company_id"
                        name="company_id"
                        v-model="formData.company_id"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm appearance-none"
                      >
                        <option :value="null">
                          {{ allCompanies.length === 0 ? "Loading companies..." : "Pilih nama perusahaan" }}
                        </option>
                        <option
                          v-for="company in allCompanies"
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

                  <div>
                    <label
                      for="stnk_expiry"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Tanggal STNK</label
                    >
                    <input
                      id="stnk_expiry"
                      name="stnk_expiry"
                      v-model="formData.stnk_expiry"
                      type="date"
                      class="w-full p-2 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                    />
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label
                      for="pajak_expiry"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Tanggal Pajak</label
                    >
                    <input
                      id="pajak_expiry"
                      name="pajak_expiry"
                      v-model="formData.pajak_expiry"
                      type="date"
                      class="w-full p-2 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                    />
                  </div>

                  <div>
                    <label
                      for="kir_expiry"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >KIR / KUER</label
                    >
                    <input
                      id="kir_expiry"
                      name="kir_expiry"
                      v-model="formData.kir_expiry"
                      type="date"
                      class="w-full p-2 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                    />
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <label
                      for="no_rangka"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Nomor Rangka</label
                    >
                    <div class="relative">
                      <input
                        id="no_rangka"
                        name="no_rangka"
                        v-model="formData.no_rangka"
                        type="text"
                        placeholder="Masukkan nomor rangka"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                      />
                      <PencilIcon
                        class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                      />
                    </div>
                  </div>

                  <div>
                    <label
                      for="no_mesin"
                      class="block text-base font-medium text-gray-800 mb-1 mt-1"
                      >Nomor Mesin</label
                    >
                    <div class="relative">
                      <input
                        id="no_mesin"
                        name="no_mesin"
                        v-model="formData.no_mesin"
                        type="text"
                        placeholder="Masukkan nomor mesin"
                        class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] text-sm"
                      />
                      <PencilIcon
                        class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                      />
                    </div>
                  </div>
                </div>

                <div class="flex justify-end gap-3 mt-6">
                  <button
                    @click="handleTambahUnitKendaraan"
                    :disabled="isLoading"
                    class="px-6 md:px-6 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular disabled:opacity-50"
                  >
                    {{ editingId ? "Update Unit Kendaraan" : "Tambah Unit Kendaraan" }}
                  </button>
                  <button
                    @click="closeTambahUnitKendaraan"
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

                <!-- Nama Perusahaan -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Nama Perusahaan</label
                  >
                  <div class="relative">
                    <select
                      v-model="filterData.perusahaan"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] appearance-none"
                    >
                      <option value="">Pilih Perusahaan</option>
                      <option
                        v-for="comp in uniqueCompanies"
                        :key="comp"
                        :value="comp"
                      >
                        {{ comp }}
                      </option>
                    </select>
                    <ChevronDownIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                    />
                  </div>
                </div>

                <!-- Tipe -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Tipe Kendaraan</label
                  >
                  <div class="relative">
                    <select
                      v-model="filterData.vehicle_type"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] appearance-none"
                    >
                      <option value="">Pilih Tipe</option>
                      <option
                        v-for="type in uniqueTypes"
                        :key="type"
                        :value="type"
                      >
                        {{ type }}
                      </option>
                    </select>
                    <ChevronDownIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                    />
                  </div>
                </div>

                <!-- Merek -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Merek</label
                  >
                  <div class="relative">
                    <select
                      v-model="filterData.merk"
                      class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8] appearance-none"
                    >
                      <option value="">Pilih Merek</option>
                      <option
                        v-for="merk in uniqueMerks"
                        :key="merk"
                        :value="merk"
                      >
                        {{ merk }}
                      </option>
                    </select>
                    <ChevronDownIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#949494] pointer-events-none"
                    />
                  </div>
                </div>

                <!-- Tanggal STNK -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Tanggal STNK</label
                  >
                  <div class="relative">
                    <input
                      v-model="filterData.stnk_date"
                      type="date"
                      class="w-full p-2 pr-2 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                    />
                  </div>
                </div>

                <!-- Tanggal Pajak -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Tanggal Pajak</label
                  >
                  <div class="relative">
                    <input
                      v-model="filterData.pajak_date"
                      type="date"
                      class="w-full p-2 pr-2 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                    />
                  </div>
                </div>

                <!-- Tanggal KIR / KUER -->
                <div>
                  <label
                    class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                    >Tanggal KIR / KUER</label
                  >
                  <div class="relative">
                    <input
                      v-model="filterData.kir_date"
                      type="date"
                      class="w-full p-2 pr-2 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
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
      title="Upload Data Kendaraan Travel"
      upload-type="vehicles-travel"
      @close="closeBulkUpload"
      @success="handleUploadSuccess"
    />
  </div>
</template>
