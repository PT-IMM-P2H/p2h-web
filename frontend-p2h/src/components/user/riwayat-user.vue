<script setup>
import NavBar from "../bar/header-user.vue";
import Footer from "../bar/footer.vue";
import { ArrowLongDownIcon, ArrowLongUpIcon } from "@heroicons/vue/24/outline";
import { ref, computed } from "vue";

const riwayatData = ref([
  {
    tanggal: "2025-01-05",
    noLambung: "P - 300",
    merek: "Toyota Innova reborn 2.4G",
    tipe: "Light Vehicle",
    nomorPolisi: "B 1234 ABC",
    hasil: "Normal"
  },
  {
    tanggal: "2025-01-04",
    noLambung: "002",
    merek: "Isuzu",
    tipe: "NPR",
    nomorPolisi: "B 5678 DEF",
    hasil: "Abnormal"
  },
  {
    tanggal: "2025-01-03",
    noLambung: "003",
    merek: "Mitsubishi",
    tipe: "Fuso",
    nomorPolisi: "B 9012 GHI",
    hasil: "Warning"
  },
  {
    tanggal: "2025-01-02",
    noLambung: "002",
    merek: "Isuzu",
    tipe: "NPR",
    nomorPolisi: "B 5678 DEF",
    hasil: "Abnormal"
  },
  {
    tanggal: "2025-01-01",
    noLambung: "002",
    merek: "Isuzu",
    tipe: "NPR",
    nomorPolisi: "B 5678 DEF",
    hasil: "Normal"
  },
  {
    tanggal: "2025-01-07",
    noLambung: "002",
    merek: "Isuzu",
    tipe: "NPR",
    nomorPolisi: "B 5678 DEF",
    hasil: "Abnormal"
  },
    {
    tanggal: "2025-01-01",
    noLambung: "002",
    merek: "Isuzu",
    tipe: "NPR",
    nomorPolisi: "B 5678 DEF",
    hasil: "Abnormal"
  },
]);

const currentPage = ref(1);
const itemsPerPage = ref(10);
const sortOrder = ref("desc");

const sortByDate = () => {
  if (sortOrder.value === "desc") {
    sortOrder.value = "asc";
    riwayatData.value = [...riwayatData.value].sort((a, b) => new Date(a.tanggal).getTime() - new Date(b.tanggal).getTime());
  } else {
    sortOrder.value = "desc";
    riwayatData.value = [...riwayatData.value].sort((a, b) => new Date(b.tanggal).getTime() - new Date(a.tanggal).getTime());
  }
  currentPage.value = 1;
};

const getHasilStyle = (hasil) => {
  const styles = {
    "Normal": { bg: "#A7E8BF", text: "#1A5C3F" },
    "Abnormal": { bg: "#F7E19C", text: "#8B6F47" },
    "Warning": { bg: "#FFA0A0", text: "#8B3A3A" }
  };
  return styles[hasil] || styles["Normal"];
};

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return riwayatData.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(riwayatData.value.length / itemsPerPage.value);
});

const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage.value + 1;
});

const endIndex = computed(() => {
  return Math.min(currentPage.value * itemsPerPage.value, riwayatData.value.length);
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
    <!-- Navbar -->
    <NavBar />

    <!-- Content -->
    <main
      class="flex-1 flex items-center justify-center bg-cover bg-center bg-no-repeat px-2 md:px-2 pt-24 md:pt-8 pb-40 md:pb-20 overflow-y-auto"
      style="background-image: url(/image_asset/Backgrond.png)"
    >
      <div
        class="w-300 h-auto flex flex-col bg-white rounded-xl shadow-lg max-w-full md:max-w-6xl p-3 md:p-7">
        <h1 class="flex justify-start text-xl md:text-2xl font-bold text-gray-800 mb-3 md:mb-4">
          Riwayat
        </h1>
        
        <!-- Table -->
        <div class="overflow-x-auto overflow-y-auto rounded-lg border bg-white max-h-[500px]">
          <table class="w-full border-collapse text-sm md:text-base">
            <thead class="sticky top-0 z-10 bg-gray-50">
              <tr class="border-b-2 border-gray-400">
                <th class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 cursor-pointer hover:bg-gray-100 transition whitespace-nowrap text-xs md:text-sm" @click="sortByDate">
                  <div class="flex items-center gap-1 md:gap-2">
                    <span>Tanggal</span>
                    <ArrowLongDownIcon v-if="sortOrder === 'desc'" class="w-3 h-3 md:w-4 md:h-4" />
                    <ArrowLongUpIcon v-else class="w-3 h-3 md:w-4 md:h-4" />
                  </div>
                </th>
                <th class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm">No. Lambung</th>
                <th class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm">Tipe</th>
                <th class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm">Merek</th>
                <th class="hidden md:table-cell px-4 py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-sm">Nomor Polisi</th>
                <th class="px-2 md:px-4 py-2 md:py-3 text-left font-semibold text-gray-700 whitespace-nowrap text-xs md:text-sm">Hasil</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in paginatedData" :key="index" class="border-b border-gray-200 hover:bg-gray-50">
                <td class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm">{{ item.tanggal }}</td>
                <td class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm">{{ item.noLambung }}</td>
                <td class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm">{{ item.tipe }}</td>
                <td class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm">{{ item.merek }}</td>
                <td class="hidden md:table-cell px-4 py-3 text-gray-800 whitespace-nowrap text-sm">{{ item.nomorPolisi }}</td>
                <td class="px-2 md:px-4 py-2 md:py-3 text-gray-800 whitespace-nowrap text-xs md:text-sm">
                  <span class="px-2 md:px-3 py-1 rounded-full text-xs md:text-sm font-semibold" :style="{ backgroundColor: getHasilStyle(item.hasil).bg, color: getHasilStyle(item.hasil).text }">
                    {{ item.hasil }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex flex-wrap justify-between items-center gap-3 pt-4 border-t border-gray-200 mt-4">
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
              {{ startIndex }} - {{ endIndex }} dari {{ riwayatData.length }}
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
