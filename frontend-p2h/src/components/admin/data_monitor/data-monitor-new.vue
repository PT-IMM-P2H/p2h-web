<script setup>
import { ref, computed } from "vue";
import Aside from "../../bar/aside.vue";
import HeaderAdmin from "../../bar/header_admin.vue";
import {
  MagnifyingGlassIcon,
  Bars3BottomLeftIcon,
  ArrowUpTrayIcon,
  TrashIcon,
  XMarkIcon,
  ChevronDownIcon,
  CalendarIcon,
  CheckIcon
} from "@heroicons/vue/24/outline";
import { useSidebarProvider } from "../../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();

const selectedRowIds = ref([]);
const selectAllChecked = ref(false);
const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = 10;
const showFilter = ref(false);
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

const applyFilter = () => {
  appliedFilterHasil.value = { ...filterHasil.value };
  currentPage.value = 1;
  closeFilter();
};

const openFilter = () => {
  showFilter.value = true;
};

const closeFilter = () => {
  showFilter.value = false;
};

const tableData = ref([
  {
    id: 1,
    tanggal: "28/12/2025",
    waktu: "08:30:00",
    noLambung: "P - 309",
    nomorPolisi: "KT 1234 KLS",
    tipe: "Light Vehicle",
    merek: "Toyota Innova reborn 2.4G",
    namaPemeriksa: "Budi Santoso",
    shift: "Shift 07.00 - 15.00",
    kategoriLayanan: "Operasional Site",
    perusahaan: "PT Indominco Mandiri",
    hasil: "Normal",
  },
  {
    id: 2,
    tanggal: "28/12/2025",
    waktu: "14:15:00",
    noLambung: "D - 002",
    nomorPolisi: "KT 5678 KLS",
    tipe: "Double Cabin",
    merek: "Volvo",
    namaPemeriksa: "Siti Nurhaliza",
    shift: "Siang",
    kategoriLayanan: "Transportasi",
    perusahaan: "PT Indominco Mandiri",
    hasil: "Abnormal",
  },
  {
    id: 3,
    tanggal: "28/12/2025",
    waktu: "22:45:00",
    noLambung: "KD-003",
    nomorPolisi: "B 9012 KLS",
    tipe: "Dump Truck",
    merek: "Isuzu",
    namaPemeriksa: "Ahmad Wijaya",
    shift: "Malam",
    kategoriLayanan: "Pertambangan",
    perusahaan: "PT Indominco Mandiri",
    hasil: "Warning",
  },
]);

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
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredTableData.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredTableData.value.length / itemsPerPage);
});

const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage + 1;
});

const endIndex = computed(() => {
  return Math.min(
    currentPage.value * itemsPerPage,
    filteredTableData.value.length
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
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <div class="flex flex-1 overflow-hidden">
      <Aside />

      <div class="flex flex-col flex-1 overflow-hidden">
        <HeaderAdmin />

        <!-- Content -->
        <main class="bg-[#EFEFEF] flex-1 flex flex-col p-3 overflow-hidden">
          <!-- Judul -->
          <div
            class="bg-white rounded-lg shadow-md p-1 pl-5 mb-2 -mt-1 shrink-0"
          >
            <h1 class="text-base font-bold text-[#523E95] text-left">
              PT Indominco Mandiri
            </h1>
          </div>
          <div
            class="bg-white rounded-lg shadow-md p-5 flex-1 flex flex-col overflow-hidden"
          >
            <!-- Toolbar -->
            <div
              class="flex items-center gap-3 pb-4 border-b shrink-0 flex-none justify-end"
            >
              <!-- Search Input with Icon Inside -->
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

              <!-- Filter Button -->
              <button
                @click="openFilter"
                class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition text-sm"
              >
                <Bars3BottomLeftIcon class="w-4 h-4" />
                <span>Filter</span>
              </button>

              <!-- Export Button -->
              <button
                class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition text-sm"
              >
                <ArrowUpTrayIcon class="w-4 h-4" />
                <span>Export</span>
              </button>

              <!-- Delete Button -->
              <button
                :disabled="selectedRowIds.length === 0"
                class="flex items-center gap-2 px-3 py-2 rounded-md transition text-sm"
                :class="
                  selectedRowIds.length > 0
                    ? 'bg-red-100 text-red-700 border border-red-300 hover:bg-red-200'
                    : 'bg-gray-100 text-gray-400 border border-gray-300 cursor-not-allowed'
                "
              >
                <TrashIcon class="w-4 h-4" />
                <span>Hapus</span>
              </button>
            </div>

            <!-- Table Container with Horizontal Scroll -->
            <div
              class="flex-1 flex flex-col gap-4 bg-gray-50 p-1 rounded-lg border border-gray-200 overflow-hidden"
            >
              <div
                class="flex-1 overflow-x-auto overflow-y-auto rounded-lg border bg-white"
              >
                <table class="w-full border-collapse">
                  <thead>
                    <tr class="border-b-2 border-gray-400 bg-gray-50">
                      <th
                        class="px-2 md:px-3 py-3 text-center font-semibold text-gray-700 whitespace-nowrap w-10 md:w-14"
                      >
                        <div class="flex items-center justify-center">
                          <div class="relative w-3.5 h-3.5 md:w-4 md:h-4">
                            <input
                              type="checkbox"
                              :checked="selectAllChecked"
                              @change="toggleSelectAll"
                              class="w-3.5 h-3.5 md:w-4 md:h-4 cursor-pointer rounded border appearance-none
                                    bg-white border-gray-500
                                    checked:bg-blue-500 checked:border-blue-500"
                              style="
                                appearance: none;
                                -webkit-appearance: none;
                              -moz-appearance: none;
                              "
                              title="Pilih semua / Batal pilih semua"
                            />
                            <!-- Check Icon -->
                            <CheckIcon
                              v-if="selectAllChecked"
                              class="absolute inset-0 m-auto w-2.5 h-2.5 md:w-3 md:h-3 text-white pointer-events-none"
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
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="row in paginatedData"
                      :key="row.id"
                      class="border-b border-gray-200 hover:bg-gray-50 transition cursor-pointer"
                      :class="{ 'bg-blue-50': isRowSelected(row.id) }">
                        <td class="px-2 md:px-3 py-3 text-center whitespace-nowrap w-10 md:w-14">
                          <div class="flex items-center justify-center">
                            <div class="relative w-3.5 h-3.5 md:w-4 md:h-4">
                              <input
                                type="checkbox"
                                :checked="isRowSelected(row.id)"
                                @change="selectRow(row.id)"
                                @click.stop
                                class="w-3.5 h-3.5 md:w-4 md:h-4 cursor-pointer rounded border appearance-none
                                      bg-white border-gray-500
                                      checked:bg-blue-500 checked:border-blue-500"/>

                              <!-- Check Icon -->
                              <CheckIcon
                                v-if="isRowSelected(row.id)"
                                class="absolute inset-0 m-auto w-2.5 h-2.5 md:w-3 md:h-3 text-white pointer-events-none"
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
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Pagination -->
              <div
                class="flex flex-col md:flex-row justify-between md:justify-end items-center gap-3 md:gap-4 pt-3 md:pt-4 border-t border-gray-200"
              >
                <span
                  class="text-xs md:text-sm text-gray-700 font-medium order-2 md:order-1"
                >
                  {{ startIndex }} - {{ endIndex }} of
                  {{ filteredTableData.length }}
                </span>
                <div class="flex gap-2 order-1 md:order-2">
                  <button
                    @click="previousPage"
                    :disabled="currentPage === 1"
                    class="px-2 md:px-3 py-1 md:py-2 border border-gray-300 rounded-md text-gray-700 font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition"
                  >
                    &lt;
                  </button>
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
                      type="text"
                      placeholder="hh / bb / tttt"
                      class="w-full p-2 pr-10 text-xs border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                    />
                    <CalendarIcon
                      class="absolute right-3 top-2.5 w-4 h-4 text-[#4b4b4b]"
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
                      type="text"
                      placeholder="hh / bb / tttt"
                      class="w-full p-2 pr-10 text-xs border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                    />
                    <CalendarIcon
                      class="absolute right-3 top-2.5 w-4 h-4 text-[#4b4b4b]"
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
                  <input
                    type="text"
                    placeholder="Pilih Perusahaan"
                    class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                  />
                  <ChevronDownIcon
                    class="absolute right-3 top-2.5 w-5 h-5 text-[#949494]"
                  />
                </div>
              </div>

              <!-- Departemen -->
              <div>
                <label class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                  >Departemen</label
                >
                <div class="relative">
                  <input
                    type="text"
                    placeholder="Pilih Departemen"
                    class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                  />
                  <ChevronDownIcon
                    class="absolute right-3 top-2.5 w-5 h-5 text-[#949494]"
                  />
                </div>
              </div>

              <!-- Departemen -->
              <div>
                <label class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                  >Posisi Kerja</label
                >
                <div class="relative">
                  <input
                    type="text"
                    placeholder="Pilih Posisi Kerja"
                    class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                  />
                  <ChevronDownIcon
                    class="absolute right-3 top-2.5 w-5 h-5 text-[#949494]"
                  />
                </div>
              </div>

              <!-- Status Kerja -->
              <div>
                <label class="block text-sm font-medium text-gray-800 mb-2 mt-2"
                  >Status Kerja</label
                >
                <div class="relative">
                  <input
                    type="text"
                    placeholder="Pilih Status Kerja"
                    class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-md focus:outline-none focus:border-[#A90CF8]"
                  />
                  <ChevronDownIcon
                    class="absolute right-3 top-2.5 w-5 h-5 text-[#949494]"
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