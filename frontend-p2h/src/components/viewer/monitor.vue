<script setup>
import { ref, computed, onMounted } from "vue";
import NavBar from "../bar/header-user.vue";
import Footer from "../bar/footer.vue";
import {
  MagnifyingGlassIcon,
  ArrowLongDownIcon,
  ArrowLongUpIcon,
} from "@heroicons/vue/24/solid";
import { api } from "../../services/api";

const nomorLambung = ref("");
const hasilPencarian = ref([]);
const selectedKendaraan = ref(null);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const sortOrder = ref("desc");
const isLoading = ref(false);

// Data P2H Reports dari backend
const p2hReports = ref([]);

// Fetch data P2H reports
const fetchP2HReports = async () => {
  try {
    isLoading.value = true;
    console.log('🔄 Fetching P2H reports...');
    const response = await api.get('/p2h/reports?limit=100');
    console.log('✅ P2H reports fetched:', response.data);
    p2hReports.value = response.data.payload;
    console.log('📊 Total reports:', p2hReports.value.length);
  } catch (error) {
    console.error('❌ Gagal fetch P2H reports:', error);
    console.error('Error details:', error.response?.data);
    if (error.response?.status === 401) {
      alert('Sesi Anda telah berakhir. Silakan login terlebih dahulu.');
      // Redirect ke login jika diperlukan
      // window.location.href = '/login';
    } else {
      alert('Gagal memuat data P2H: ' + (error.response?.data?.detail || error.message));
    }
  } finally {
    isLoading.value = false;
  }
};

// Format data untuk riwayat table
const riwayatData = computed(() => {
  return p2hReports.value.map(report => ({
    id: report.id,
    tanggal: report.submission_date,
    waktu: report.submission_time,
    shift: report.shift_number,
    nomor: report.vehicle.no_lambung,
    warnaLambung: report.vehicle.warna_no_lambung || '-',
    merek: report.vehicle.merk,
    tipe: report.vehicle.vehicle_type,
    platKendaraan: report.vehicle.plat_nomor,
    hasil: report.overall_status,
    status: report.overall_status === 'normal' ? 'Normal' : 
            report.overall_status === 'abnormal' ? 'Abnormal' : 'Warning',
    user: report.user.full_name
  }));
});


const handleCariKendaraan = () => {
  if (nomorLambung.value.trim()) {
    const normalizedInput = nomorLambung.value.toLowerCase().replace(/[\s.-]/g, "");
    
    hasilPencarian.value = riwayatData.value.filter((report) => {
      const normalizedNomor = report.nomor.toLowerCase().replace(/[\s.-]/g, "");
      return normalizedNomor.includes(normalizedInput);
    });
  } else {
    hasilPencarian.value = [];
  }
};

const handleSelectKendaraan = (kendaraan) => {
  selectedKendaraan.value = kendaraan;
};

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

// Get hasil style
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

// Pagination computed
const totalPages = computed(() =>
  Math.ceil(sortedRiwayatData.value.length / itemsPerPage.value)
);
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return sortedRiwayatData.value.slice(start, end);
});

const startIndex = computed(
  () => (currentPage.value - 1) * itemsPerPage.value + 1
);
const endIndex = computed(() =>
  Math.min(currentPage.value * itemsPerPage.value, sortedRiwayatData.value.length)
);

// Pagination functions
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
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
      class="flex-1 flex flex-col bg-cover bg-center bg-no-repeat px-2 md:px-2 pt-24 md:pt-8 pb-40 md:pb-20 overflow-y-auto"
      style="background-image: url(/image_asset/BG_2.png)"
    >
      <div class="flex flex-col items-center gap-4 w-full">
        <!-- Konten Utama -->
        <div
          class="mt-15 w-300 h-auto flex flex-col bg-white rounded-xl shadow-lg max-w-full md:max-w-5xl p-3 md:p-7"
        >
          <h1 class="text-2xl font-bold mb-2 text-gray-800 text-left">
            Jenis kendaraan
          </h1>
          <hr class="border-t-3 border-[#9600E1] rounded-lg mb-4" />
          <div class="flex flex-col gap-4">
            <div class="flex gap-3 items-center">
              <div class="relative flex-1">
                <input
                  v-model="nomorLambung"
                  type="text"
                  placeholder="Nomor Lambung Kendaraan"
                  @input="handleCariKendaraan"
                  @keyup.enter="handleCariKendaraan"
                  class="w-full px-3.75 py-3 pr-10 border border-[#a1a1a1] bg-gray-100 rounded-lg text-[14px] text-[#333] transition-colors duration-300 focus:outline-none focus:border-[#646cff] focus:ring-3 focus:ring-[#646cff]/10"
                />
                <MagnifyingGlassIcon
                  class="absolute right-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500 pointer-events-none"
                />
              </div>
              <button
                @click="handleCariKendaraan"
                class="px-13 py-3 bg-[#9600E1] text-white rounded-lg text-base font-semibold cursor-pointer transition-colors duration-300 hover:bg-[#8507c5] whitespace-nowrap active:bg-[#3a276b]"
              >
                Cari
              </button>
            </div>
          </div>

          <!-- HASIL PENCARIAN DATA -->
          <div
            v-if="hasilPencarian.length > 0"
            class="flex flex-col gap-4 mt-4"
          >
            <div
              v-for="kendaraan in hasilPencarian.filter(
                (k) => k.status === 'sudah'
              )"
              :key="kendaraan.id"
              class="w-auto h-auto flex flex-col border-2 border-[#2DA642] bg-[#C5FFCF] rounded-xl shadow-lg max-w-full md:max-w-5xl p-4 md:p-4 gap-2"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <p class="text-sm text-gray-700">Nomor lambung : <span class="font-semibold">{{ kendaraan.nomor }}</span></p>
                  <p class="text-sm text-gray-700">Warna nomor lambung : <span class="font-semibold">{{ kendaraan.warnaLambung }}</span></p>
                  <p class="text-sm text-gray-700">Merek Kendaraan : <span class="font-semibold">{{ kendaraan.merek }}</span></p>
                  <p class="text-sm text-gray-700">Tipe Kendaraan : <span class="font-semibold">{{ kendaraan.tipe }}</span></p>
                  <p class="text-sm text-gray-700">Plat Kendaraan : <span class="font-semibold">{{ kendaraan.platKendaraan }}</span></p>
                </div>
                <button
                  @click="handleSelectKendaraan(kendaraan)"
                  class="px-4 py-10 bg-[#2eb745] text-white rounded-lg text-xs md:text-sm font-semibold cursor-pointer transition-colors duration-300 hover:bg-[#24a635] whitespace-nowrap ml-3"
                >
                  SELECT
                </button>
              </div>
            </div>
            <div
              v-for="kendaraan in hasilPencarian.filter(
                (k) => k.status === 'belum'
              )"
              :key="kendaraan.id"
              class="w-auto h-auto flex flex-col border-2 border-[#A62D2D] bg-[#FFC5C5] rounded-xl shadow-lg max-w-full md:max-w-5xl p-4 md:p-4 gap-2"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <p class="text-sm text-gray-700">Nomor lambung : <span class="font-semibold">{{ kendaraan.nomor }}</span></p>
                  <p class="text-sm text-gray-700">Warna nomor lambung : <span class="font-semibold">{{ kendaraan.warnaLambung }}</span></p>
                  <p class="text-sm text-gray-700">Merek Kendaraan : <span class="font-semibold">{{ kendaraan.merek }}</span></p>
                  <p class="text-sm text-gray-700">Tipe Kendaraan : <span class="font-semibold">{{ kendaraan.tipe }}</span></p>
                  <p class="text-sm text-gray-700">Plat Kendaraan : <span class="font-semibold">{{ kendaraan.platKendaraan }}</span></p>
                </div>
                <button
                  @click="handleSelectKendaraan(kendaraan)"
                  class="px-4 py-10 bg-[#A62D2D] text-white rounded-lg text-xs md:text-sm font-semibold cursor-pointer transition-colors duration-300 hover:bg-[#8b2424] whitespace-nowrap ml-3"
                >
                  SELECT
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Hasil Sudah P2H -->
        <div
          v-if="selectedKendaraan && selectedKendaraan.status === 'sudah'"
          class="w-300 h-auto flex flex-col border-2 border-[#2DA642] bg-[#C5FFCF] rounded-xl shadow-lg max-w-full md:max-w-5xl p-3 md:p-3"
        >
          <p class="font-bold text-black">
            SUDAH DI LAKUKAN PELAKSANAAN PEMERIKSAAN HARIAN
          </p>
        </div>

        <!-- Hasil Belum P2H -->
        <div v-if="selectedKendaraan && selectedKendaraan.status === 'belum'">
          <div
            class="w-300 h-auto flex flex-col border-2 border-[#A62D2D] bg-[#FFC5C5] rounded-xl shadow-lg max-w-full md:max-w-5xl p-3 md:p-3"
          >
            <p class="font-bold text-black">
              BELUM DI LAKUKAN PELAKSANAAN PEMERIKSAAN HARIAN
            </p>
          </div>
          <!-- Button FORM P2H -->
          <div class="w-300 mt-4 flex justify-end max-w-full md:max-w-5xl">
            <button
              class="px-10 py-3 bg-[#9600E1] text-white rounded-xl text-[14px] font-semibold cursor-pointer transition-colors duration-300 hover:bg-[#8507c5] whitespace-nowrap"
            >
              FORM P2H
            </button>
          </div>
        </div>

        <!-- Hidden Riwayat Kendaraan -->
        <div
          class="w-300 h-auto flex flex-col bg-white rounded-xl shadow-lg max-w-full md:max-w-5xl p-3 md:p-7 mb-15"
        >
          <h1
            class="flex justify-start text-xl md:text-2xl font-bold text-gray-800 mb-3 md:mb-4"
          >
            Riwayat
          </h1>

          <!-- Table -->
          <div
            class="overflow-x-auto -mx-3 md:mx-0 md:rounded-lg border-b md:border flex-1 mb-3 md:mb-4"
          >
            <table class="w-full border-collapse text-sm md:text-base">
              <thead>
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
                    Warna Lambung
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
                    class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm"
                  >
                    Plat Kendaraan
                  </th>
                  <th
                    class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm"
                  >
                    User
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
                  <td colspan="10" class="px-4 py-8 text-center text-gray-500">
                    <div class="flex items-center justify-center gap-2">
                      <svg class="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <span class="font-semibold">Memuat data...</span>
                    </div>
                  </td>
                </tr>
                
                <!-- Empty State -->
                <tr v-else-if="!isLoading && paginatedData.length === 0">
                  <td colspan="10" class="px-4 py-8 text-center text-gray-500">
                    <div class="flex flex-col items-center gap-2">
                      <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                      <p class="font-semibold text-lg">Belum ada data P2H</p>
                      <p class="text-sm">Data akan muncul setelah ada laporan P2H yang disubmit</p>
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
                    {{ item.nomor }}
                  </td>
                  <td
                    class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                  >
                    {{ item.warnaLambung }}
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
                    class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                  >
                    {{ item.platKendaraan }}
                  </td>
                  <td
                    class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm"
                  >
                    {{ item.user }}
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
            class="flex flex-col md:flex-row justify-between md:justify-end items-center gap-3 md:gap-4 pt-3 md:pt-4 border-t border-gray-200"
          >
            <span
              class="text-xs md:text-sm text-gray-700 font-medium order-2 md:order-1"
            >
              {{ startIndex }} - {{ endIndex }} of {{ riwayatData.length }}
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
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>