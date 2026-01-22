<script setup>
import NavBar from "../bar/header-user.vue";
import Footer from "../bar/footer.vue";
import { ArrowLongDownIcon, ArrowLongUpIcon } from "@heroicons/vue/24/outline";
import { ref, computed, onMounted } from "vue";
import { api } from "../../services/api";

const currentPage = ref(1);
const itemsPerPage = ref(10);
const sortOrder = ref("desc");
const isLoading = ref(false);

// Data P2H Reports dari backend
const p2hReports = ref([]);

// Fetch data P2H reports untuk user yang sedang login
const fetchP2HReports = async () => {
  try {
    isLoading.value = true;
    console.log("🔄 Fetching user P2H reports...");
    const response = await api.get("/p2h/reports?limit=100");
    console.log("✅ User P2H reports fetched:", response.data);
    p2hReports.value = response.data.payload;
    console.log("📊 Total reports:", p2hReports.value.length);
  } catch (error) {
    console.error("❌ Gagal fetch P2H reports:", error);
    console.error("Error details:", error.response?.data);
    if (error.response?.status === 401) {
      alert("Sesi Anda telah berakhir. Silakan login terlebih dahulu.");
      // Redirect ke login jika diperlukan
      // window.location.href = '/login';
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

// Format data untuk riwayat table
const riwayatData = computed(() => {
  return p2hReports.value.map((report) => ({
    id: report.id,
    tanggal: report.submission_date,
    waktu: report.submission_time,
    shift: report.shift_number,
    noLambung: report.vehicle.no_lambung,
    warnaLambung: report.vehicle.warna_no_lambung || "-",
    merek: report.vehicle.merk,
    tipe: report.vehicle.vehicle_type,
    nomorPolisi: report.vehicle.plat_nomor,
    hasil:
      report.overall_status === "normal"
        ? "Normal"
        : report.overall_status === "abnormal"
          ? "Abnormal"
          : "Warning",
  }));
});

// Sort function
const sortByDate = () => {
  sortOrder.value = sortOrder.value === "desc" ? "asc" : "desc";
};

// Computed sorted data
const sortedRiwayatData = computed(() => {
  const data = [...riwayatData.value];
  return data.sort((a, b) => {
    const dateA = new Date(`${a.tanggal}T${a.waktu}`);
    const dateB = new Date(`${b.tanggal}T${b.waktu}`);
    return sortOrder.value === "desc" ? dateB - dateA : dateA - dateB;
  });
});

const getHasilStyle = (hasil) => {
  const styles = {
    Normal: { bg: "#A7E8BF", text: "#1A5C3F" },
    normal: { bg: "#A7E8BF", text: "#1A5C3F" },
    Abnormal: { bg: "#F7E19C", text: "#8B6F47" },
    abnormal: { bg: "#F7E19C", text: "#8B6F47" },
    Warning: { bg: "#FFA0A0", text: "#8B3A3A" },
    warning: { bg: "#FFA0A0", text: "#8B3A3A" },
  };
  return styles[hasil] || styles["Normal"];
};

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return sortedRiwayatData.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(sortedRiwayatData.value.length / itemsPerPage.value);
});

const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage.value + 1;
});

const endIndex = computed(() => {
  return Math.min(
    currentPage.value * itemsPerPage.value,
    sortedRiwayatData.value.length,
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

// Fetch data on mount
onMounted(() => {
  fetchP2HReports();
});
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <!-- Navbar -->
    <NavBar />

    <!-- Content -->
    <main
      class="flex-1 flex items-center justify-center bg-cover bg-center bg-no-repeat px-2 md:px-2 pt-24 md:pt-8 pb-40 md:pb-20 overflow-y-auto"
      style="background-image: url(/image_asset/BG_2.png)"
    >
      <div
        class="w-300 h-auto flex flex-col bg-white rounded-xl shadow-lg max-w-full md:max-w-6xl p-3 md:p-7"
      >
        <h1
          class="flex justify-start text-xl md:text-2xl font-bold text-gray-800 mb-3 md:mb-4"
        >
          Riwayat
        </h1>

        <!-- Table -->
        <div
          class="overflow-x-auto overflow-y-auto rounded-lg border bg-white max-h-[500px]"
        >
          <table class="w-full border-collapse text-sm md:text-base">
            <thead class="sticky top-0 z-10 bg-gray-50">
              <tr class="border-b-2 border-gray-400">
                <th
                  class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 cursor-pointer hover:bg-gray-100 transition whitespace-nowrap text-xs md:text-sm"
                  @click="sortByDate"
                >
                  <div class="flex items-center gap-1 md:gap-2">
                    <span>Tanggal</span>
                    <ArrowLongDownIcon
                      v-if="sortOrder === 'desc'"
                      class="w-3 h-3 md:w-4 md:h-4"
                    />
                    <ArrowLongUpIcon v-else class="w-3 h-3 md:w-4 md:h-4" />
                  </div>
                </th>
                <th
                  class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm"
                >
                  Waktu
                </th>
                <th
                  class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm"
                >
                  Shift
                </th>
                <th
                  class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm"
                >
                  No. Lambung
                </th>
                <th
                  class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm"
                >
                  Tipe
                </th>
                <th
                  class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm"
                >
                  Merek
                </th>
                <th
                  class="hidden md:table-cell px-4 py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-sm"
                >
                  Nomor Polisi
                </th>
                <th
                  class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm"
                >
                  Hasil
                </th>
              </tr>
            </thead>
            <tbody>
              <!-- Loading State -->
              <tr v-if="isLoading">
                <td colspan="8" class="px-4 py-8 text-center text-gray-500">
                  <div class="flex items-center justify-center gap-2">
                    <svg
                      class="animate-spin h-5 w-5 text-blue-600"
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
                    <span class="font-semibold">Memuat data...</span>
                  </div>
                </td>
              </tr>

              <!-- Empty State -->
              <tr v-else-if="!isLoading && paginatedData.length === 0">
                <td colspan="8" class="px-4 py-8 text-center text-gray-500">
                  <div class="flex flex-col items-center gap-2">
                    <svg
                      class="w-12 h-12 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      ></path>
                    </svg>
                    <p class="font-semibold text-lg">Belum ada riwayat P2H</p>
                    <p class="text-sm">
                      Riwayat akan muncul setelah Anda mengisi form P2H
                    </p>
                  </div>
                </td>
              </tr>

              <!-- Data Rows -->
              <tr
                v-else
                v-for="(item, index) in paginatedData"
                :key="index"
                class="border-b border-gray-200 hover:bg-gray-50"
              >
                <td
                  class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                >
                  {{ item.tanggal }}
                </td>
                <td
                  class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                >
                  {{ item.waktu }}
                </td>
                <td
                  class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                >
                  {{ item.shift }}
                </td>
                <td
                  class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                >
                  {{ item.noLambung }}
                </td>
                <td
                  class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                >
                  {{ item.tipe }}
                </td>
                <td
                  class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                >
                  {{ item.merek }}
                </td>
                <td
                  class="hidden md:table-cell px-4 py-3 text-gray-800 whitespace-nowrap text-sm"
                >
                  {{ item.nomorPolisi }}
                </td>
                <td
                  class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                >
                  <span
                    class="px-2 md:px-3 py-1 rounded-full text-xs md:text-sm font-semibold"
                    :style="{
                      backgroundColor: getHasilStyle(item.hasil).bg,
                      color: getHasilStyle(item.hasil).text,
                    }"
                  >
                    {{ item.hasil }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div
          class="flex flex-wrap justify-between items-center gap-3 pt-4 border-t border-gray-200 mt-4"
        >
          <!-- Items per page selector -->
          <div class="flex items-center gap-2 text-sm text-gray-700">
            <span>Tampilkan</span>
            <select
              v-model="itemsPerPage"
              @change="currentPage = 1"
              class="px-2 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option :value="5">5</option>
              <option :value="10">10</option>
              <option :value="20">20</option>
              <option :value="50">50</option>
            </select>
            <span>baris</span>
          </div>

          <!-- Navigation -->
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
              {{ sortedRiwayatData.length }}
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
      </div>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>
