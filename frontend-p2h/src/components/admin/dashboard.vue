<script setup>
import Aside from "../bar/aside.vue";
import HeaderAdmin from "../bar/header_admin.vue";
import CardDetailModal from "./CardDetailModal.vue";
import { UserIcon, ChevronDownIcon } from "@heroicons/vue/24/outline";
import {
  onMounted,
  onBeforeUnmount,
  ref,
  nextTick,
  watch,
  computed,
} from "vue";
import Chart from "chart.js/auto";
import { useI18n } from "vue-i18n";
import { api } from "../../services/api";
import apiService from "../../services/api";
import { useSidebarProvider } from "../../composables/useSidebar";

const { t } = useI18n();

// Setup sidebar state
const { isSidebarOpen, closeSidebar } = useSidebarProvider();

let chartInstance = null;
let pieChartInstance = null;
let vehicleTypeChartInstance = null;

// Variables for date inputs (format YYYY-MM-DD untuk date picker di Filter Hari)
const a = ref("");
const u = ref("");

// Variables for month inputs (format YYYY-MM untuk month picker di Grafik Tahunan)
const annualStartPeriod = ref("2025-01");
const annualEndPeriod = ref("2026-01");

// Data statistik dari backend
const statisticsData = ref({
  totalVehicles: 0,
  totalNormal: 0,
  totalAbnormal: 0,
  totalWarning: 0,
  totalCompletedP2H: 0,
  totalPendingP2H: 0,
});

// Modal state
const modalOpen = ref(false);
const modalCardType = ref("");
const modalCardTitle = ref("");
const modalItems = ref([]);
const modalLoading = ref(false);

// Function to open modal with card details
const openCardDetail = async (cardType, cardTitle) => {
  modalCardType.value = cardType;
  modalCardTitle.value = cardTitle;
  modalOpen.value = true;
  modalLoading.value = true;

  try {
    const params = {};

    // Add date filters if set
    if (a.value && a.value !== "") {
      params.start_date = a.value;
    }
    if (u.value && u.value !== "") {
      params.end_date = u.value;
    }

    params.limit = 500; // Get more items for modal pagination

    const response = await api.get(`/dashboard/card-details/${cardType}`, {
      params,
    });
    console.log("Card details response:", response.data);

    if (response.data.status === "success") {
      modalItems.value = response.data.payload.items || [];
    }
  } catch (error) {
    console.error("Error fetching card details:", error);
    modalItems.value = [];
  } finally {
    modalLoading.value = false;
  }
};

// Close modal
const closeModal = () => {
  modalOpen.value = false;
  modalCardType.value = "";
  modalCardTitle.value = "";
  modalItems.value = [];
};

// Variables for vehicle type dropdown
const isVehicleTypeOpen = ref(false);
const selectedVehicleType = ref("");
const vehicleTypes = ref([]);

// Data bulanan dari backend
const vehicleDataByMonth = ref({
  Januari: [0, 0, 0],
  Februari: [0, 0, 0],
  Maret: [0, 0, 0],
  April: [0, 0, 0],
  Mei: [0, 0, 0],
  Juni: [0, 0, 0],
  Juli: [0, 0, 0],
  Agustus: [0, 0, 0],
  September: [0, 0, 0],
  Oktober: [0, 0, 0],
  November: [0, 0, 0],
  Desember: [0, 0, 0],
});

// Fetch dashboard statistics dari backend
const fetchStatistics = async () => {
  try {
    const params = {};

    // Add date filters if set
    if (a.value && a.value !== "") {
      params.start_date = a.value;
    }
    if (u.value && u.value !== "") {
      params.end_date = u.value;
    }

    // NOTE: Vehicle type filter NOT applied here - cards and pie chart show ALL data
    // Vehicle type filter only affects monthly chart and vehicle type status

    const response = await api.get("/dashboard/statistics", { params });
    console.log("Statistics response:", response.data);
    if (response.data.status === "success") {
      const data = response.data.payload;
      console.log("📊 Statistics data:", data);

      // Map snake_case dari backend ke camelCase untuk frontend
      statisticsData.value = {
        totalVehicles: data.total_vehicles,
        totalNormal: data.total_normal,
        totalAbnormal: data.total_abnormal,
        totalWarning: data.total_warning,
        totalCompletedP2H: data.total_completed_p2h,
        totalPendingP2H: data.total_pending_p2h,
      };

      // Update pie chart dengan data statistik
      const pieData = [
        data.total_normal || 0,
        data.total_abnormal || 0,
        data.total_warning || 0,
      ];
      console.log("🥧 Updating pie chart with data:", pieData);

      pieChartData.value.datasets[0].data = pieData;

      // Reinit pie chart setelah data berubah
      await nextTick();
      initPieChart();
    }
  } catch (error) {
    console.error("Error fetching statistics:", error);
  } finally {
    // Cleanup if needed
  }
};

// Fetch total vehicles dari vehicles table (unit-pt dan unit-travel)
const fetchTotalVehicles = async () => {
  try {
    console.log("📊 Fetching total vehicles from all units...");
    const response = await apiService.vehicles.getAll({ limit: 1000 });
    
    if (response.data.status === "success" || response.data.success) {
      const allVehicles = response.data.payload;
      const totalCount = allVehicles.length;
      
      console.log("✅ Total vehicles fetched:", totalCount);
      
      // Update totalVehicles dalam statisticsData
      statisticsData.value.totalVehicles = totalCount;
    } else {
      console.error("Failed to fetch vehicles:", response.data);
    }
  } catch (error) {
    console.error("❌ Error fetching total vehicles:", error);
  } finally {
    // Cleanup if needed
  }
};

// Fetch monthly reports dari backend
const fetchMonthlyReports = async () => {
  try {
    const currentYear = new Date().getFullYear();
    const params = {
      year: currentYear,
    };

    if (selectedVehicleType.value && selectedVehicleType.value !== "") {
      params.vehicle_type = selectedVehicleType.value;
    }

    const response = await api.get("/dashboard/monthly-reports", { params });
    console.log("Monthly reports response:", response.data);
    if (response.data.status === "success") {
      vehicleDataByMonth.value = response.data.payload.monthly_data;
      console.log("Updated vehicleDataByMonth:", vehicleDataByMonth.value);

      // Update chart setelah data berubah
      await nextTick();
      updateChart();
    }
  } catch (error) {
    console.error("Error fetching monthly reports:", error);
  } finally {
    // Cleanup if needed
  }
};

// Fetch vehicle types dari backend
const fetchVehicleTypes = async () => {
  try {
    console.log("🚗 Fetching vehicle types...");
    const response = await api.get("/dashboard/vehicle-types");
    console.log("Vehicle types response:", response.data);
    if (response.data.status === "success") {
      vehicleTypes.value = response.data.payload.vehicle_types;
      console.log("✅ Vehicle types loaded:", vehicleTypes.value);
    } else {
      console.error("❌ Failed to fetch vehicle types:", response.data);
    }
  } catch (error) {
    console.error("❌ Error fetching vehicle types:", error);
  } finally {
    // Cleanup if needed
  }
};

// Convert monthly data to Chart.js format
const convertMonthlyDataToChartFormat = (monthlyData) => {
  // Handle jika monthlyData kosong atau bukan object
  if (!monthlyData || typeof monthlyData !== "object") {
    console.warn("Invalid monthlyData:", monthlyData);
    return {
      labels: [],
      datasets: [],
    };
  }

  const months = Object.keys(monthlyData);
  const normalData = [];
  const abnormalData = [];
  const warningData = [];

  months.forEach((month) => {
    const dataArray = monthlyData[month];
    // Pastikan dataArray adalah array
    if (Array.isArray(dataArray) && dataArray.length >= 3) {
      const [normal, abnormal, warning] = dataArray;
      normalData.push(normal || 0);
      abnormalData.push(abnormal || 0);
      warningData.push(warning || 0);
    } else {
      // Jika bukan array atau kurang dari 3 elemen, isi dengan 0
      normalData.push(0);
      abnormalData.push(0);
      warningData.push(0);
    }
  });

  return {
    labels: months,
    datasets: [
      {
        label: "Normal",
        data: normalData,
        borderColor: "#10B981",
        backgroundColor: "rgba(16, 185, 129, 0.08)",
        borderWidth: 3,
        tension: 0.5,
        fill: true,
        pointBackgroundColor: "#10B981",
        pointBorderColor: "#fff",
        pointBorderWidth: 1,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointHoverBorderWidth: 3,
        segment: {
          borderDash: [],
        },
      },
      {
        label: "Abnormal",
        data: abnormalData,
        borderColor: "#F59E0B",
        backgroundColor: "rgba(245, 158, 11, 0.08)",
        borderWidth: 3,
        tension: 0.5,
        fill: true,
        pointBackgroundColor: "#F59E0B",
        pointBorderColor: "#fff",
        pointBorderWidth: 1,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointHoverBorderWidth: 3,
        segment: {
          borderDash: [],
        },
      },
      {
        label: "Warning",
        data: warningData,
        borderColor: "#EF4444",
        backgroundColor: "rgba(239, 68, 68, 0.08)",
        borderWidth: 3,
        tension: 0.5,
        fill: true,
        pointBackgroundColor: "#EF4444",
        pointBorderColor: "#fff",
        pointBorderWidth: 1,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointHoverBorderWidth: 3,
        segment: {
          borderDash: [],
        },
      },
    ],
  };
};

const vehicleData = convertMonthlyDataToChartFormat(vehicleDataByMonth);

// Function untuk menghitung nilai maksimal dari data dan tambahkan 20
const getMaxValue = (data) => {
  let max = 0;
  data.datasets.forEach((dataset) => {
    const datasetMax = Math.max(...dataset.data);
    if (datasetMax > max) max = datasetMax;
  });
  return max + 20;
};

const getChartOptions = (data) => {
  const maxValue = getMaxValue(data);
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 2000,
      easing: "easeInOutQuart",
      delay: (context) => {
        let delay = 0;
        if (context.type === "data") {
          delay = context.dataIndex * 50 + context.datasetIndex * 100;
        }
        return delay;
      },
    },
    plugins: {
      legend: {
        display: false,
        position: "top",
        labels: {
          usePointStyle: true,
          padding: 5,
          font: {
            size: 13,
            weight: "600",
            family: "'Montserrat', sans-serif",
          },
          color: "#374151",
        },
      },
      filler: {
        propagate: true,
      },
      tooltip: {
        backgroundColor: "rgba(0, 0, 0, 0.9)",
        padding: 14,
        titleFont: {
          size: 14,
          weight: "600",
        },
        bodyFont: {
          size: 13,
        },
        borderColor: "#3B82F6",
        borderWidth: 1,
        displayColors: true,
        padding: {
          top: 12,
          left: 14,
          right: 14,
          bottom: 12,
        },
        caretSize: 8,
        caretPadding: 12,
        cornerRadius: 6,
        callbacks: {
          label: function (context) {
            return " " + context.dataset.label + ": " + context.parsed.y;
          },
          afterLabel: function (context) {
            const data = context.parsed.y;
            const previous =
              context.dataIndex > 0
                ? context.chart.data.datasets[context.datasetIndex].data[context.dataIndex - 1]
                : data;
            const change = data - previous;
            const changeText =
              change > 0
                ? `↑ +${change}`
                : change < 0
                  ? `↓ ${change}`
                  : "→ Stabil";
            return changeText;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: maxValue,
        ticks: {
          stepSize: 20,
          font: {
            size: 12,
            weight: "500",
          },
          color: "#6B7280",
          padding: 8,
        },
        grid: {
          color: "rgba(200, 200, 200, 10)",
          drawBorder: false,
          lineWidth: 1,
        },
        border: {
          display: false,
        },
      },
      x: {
        ticks: {
          font: {
            size: 12,
            weight: "500",
          },
          color: "#6B7280",
          padding: 8,
        },
        grid: {
          display: false,
          drawBorder: false,
        },
        border: {
          display: false,
        },
      },
    },
    interaction: {
      mode: "index",
      intersect: false,
    },
  };
};

// Data untuk chart status berdasarkan tipe kendaraan dari backend
const vehicleTypeStatusData = ref({
  labels: ["Normal", "Abnormal", "Warning"],
  datasets: [
    {
      data: [0, 0, 0],
      backgroundColor: [
        "rgba(16, 185, 129, 0.7)",
        "rgba(245, 158, 11, 0.7)",
        "rgba(239, 68, 68, 0.7)",
      ],
      borderColor: [
        "rgba(16, 185, 129, 1)",
        "rgba(245, 158, 11, 1)",
        "rgba(239, 68, 68, 1)",
      ],
      borderWidth: 2,
    },
  ],
});

// Fetch status berdasarkan tipe kendaraan dari backend
const fetchVehicleTypeStatus = async () => {
  if (!selectedVehicleType.value) {
    return;
  }

  try {
    const params = {
      vehicle_type: selectedVehicleType.value,
    };

    const response = await api.get("/dashboard/vehicle-type-status", {
      params,
    });
    console.log("Vehicle type status response:", response.data);
    if (response.data.status === "success") {
      const data = response.data.payload;
      vehicleTypeStatusData.value.datasets[0].data = [
        data.normal || 0,
        data.abnormal || 0,
        data.warning || 0,
      ];

      // Reinit chart setelah data berubah
      await nextTick();
      initVehicleTypeChart();
    }
  } catch (error) {
    console.error("Error fetching vehicle type status:", error);
  } finally {
    // Cleanup if needed
  }
};

const pieChartData = ref({
  labels: ["Normal", "Abnormal", "Warning"],
  datasets: [
    {
      data: [0, 0, 0],
      backgroundColor: [
        "rgba(16, 185, 129, 0.7)",
        "rgba(245, 158, 11, 0.7)",
        "rgba(239, 68, 68, 0.7)",
      ],
      borderColor: [
        "rgba(16, 185, 129, 1)",
        "rgba(245, 158, 11, 1)",
        "rgba(239, 68, 68, 1)",
      ],
      borderWidth: 2,
    },
  ],
});

const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "bottom",
      labels: {
        font: {
          size: 12,
          weight: "500",
        },
        padding: 20,
        color: "#374151",
        generateLabels: (chart) => {
          const data = chart.data;
          const dataset = data.datasets[0];
          const total = dataset.data.reduce((a, b) => a + b, 0);

          return data.labels.map((label, index) => {
            const value = dataset.data[index];
            const percentage =
              total > 0 ? ((value / total) * 100).toFixed(1) : "0.0";
            return {
              text: `: ${label} ${percentage}%`,
              fillStyle: dataset.backgroundColor[index],
              strokeStyle: dataset.borderColor[index],
              borderWidth: 2,
              hidden: false,
              index: index,
              pointStyle: "circle",
            };
          });
        },
      },
    },
    tooltip: {
      backgroundColor: "rgba(0, 0, 0, 0.9)",
      padding: 12,
      titleFont: {
        size: 13,
        weight: "600",
      },
      bodyFont: {
        size: 12,
      },
      borderColor: "#10B981",
      borderWidth: 1,
      cornerRadius: 6,
      callbacks: {
        label: function (context) {
          const total = context.dataset.data.reduce((a, b) => a + b, 0);
          const value = context.parsed;
          const percentage =
            total > 0 ? ((value / total) * 100).toFixed(1) : "0.0";
          return context.label + ": " + value + " unit (" + percentage + "%)";
        },
      },
    },
  },
};

const initChart = async () => {
  // Tunggu DOM ready
  await nextTick();

  const canvas = document.getElementById("chart-vehicles");
  if (!canvas) {
    console.error("Canvas element not found");
    return;
  }

  // Destroy existing chart if it exists
  if (chartInstance) {
    try {
      chartInstance.destroy();
    } catch (error) {
      console.warn("Error destroying chart:", error);
    }
    chartInstance = null;
  }

  // Convert data
  const vehicleData = convertMonthlyDataToChartFormat(vehicleDataByMonth.value);

  // Create new chart
  try {
    chartInstance = new Chart(canvas, {
      type: "line",
      data: vehicleData,
      options: getChartOptions(vehicleData),
    });
  } catch (error) {
    console.error("Error creating chart:", error);
  }
};

const initPieChart = async () => {
  // Tunggu DOM ready
  await nextTick();

  const pieCanvas = document.getElementById("chart-pie-hasil");
  if (!pieCanvas) {
    console.error("❌ Pie chart canvas element not found");
    return;
  }

  // Destroy existing pie chart if it exists
  if (pieChartInstance) {
    console.log("🔄 Destroying existing pie chart instance");
    try {
      pieChartInstance.destroy();
    } catch (error) {
      console.warn("Error destroying pie chart:", error);
    }
    pieChartInstance = null;
  }

  // Create new pie chart
  try {
    console.log(
      "✅ Creating pie chart with data:",
      pieChartData.value.datasets[0].data,
    );
    pieChartInstance = new Chart(pieCanvas, {
      type: "pie",
      data: pieChartData.value,
      options: pieChartOptions,
    });
    console.log("✅ Pie chart created successfully");
  } catch (error) {
    console.error("❌ Error creating pie chart:", error);
  }
};

const initVehicleTypeChart = async () => {
  // Destroy existing chart if it exists
  if (vehicleTypeChartInstance) {
    console.log("🔄 Destroying existing vehicle type chart instance");
    try {
      vehicleTypeChartInstance.destroy();
    } catch (error) {
      console.warn("Error destroying vehicle type chart:", error);
    }
    vehicleTypeChartInstance = null;
  }

  // Jika belum dipilih, jangan buat chart
  if (!selectedVehicleType.value) {
    console.log("⚠️ No vehicle type selected, skipping chart creation");
    return;
  }

  // Tunggu DOM ready
  await nextTick();

  const vehicleTypeCanvas = document.getElementById("chart-pie-vehicle-type");
  if (!vehicleTypeCanvas) {
    console.error("❌ Vehicle type chart canvas element not found");
    return;
  }

  // Create new chart dengan data dari backend
  try {
    console.log(
      "✅ Creating vehicle type chart with data:",
      vehicleTypeStatusData.value.datasets[0].data,
    );
    vehicleTypeChartInstance = new Chart(vehicleTypeCanvas, {
      type: "pie",
      data: vehicleTypeStatusData.value,
      options: pieChartOptions,
    });
    console.log("✅ Vehicle type chart created successfully");
  } catch (error) {
    console.error("❌ Error creating vehicle type chart:", error);
  }
};

// Watch selectedVehicleType untuk update chart dan fetch data baru
// NOTE: fetchStatistics NOT called here - cards and main pie chart are NOT filtered by vehicle type
watch(selectedVehicleType, () => {
  if (chartInstance || pieChartInstance) {
    fetchMonthlyReports(); // Update monthly chart with vehicle type filter
    fetchVehicleTypeStatus(); // Update vehicle type status pie chart
  }
});

// Watch date filters untuk auto-update saat tanggal berubah
watch([a, u], () => {
  console.log("📅 Date filter changed:", { start: a.value, end: u.value });
  // Auto fetch data saat tanggal berubah
  if ((a.value || u.value) && (chartInstance || pieChartInstance)) {
    fetchStatistics();
    fetchMonthlyReports();
  }
});

// Update chart dengan data baru
const updateChart = () => {
  if (!chartInstance) {
    // Jika chart belum ada atau sudah di-destroy, buat baru
    initChart();
    return;
  }

  const newData = convertMonthlyDataToChartFormat(vehicleDataByMonth.value);
  chartInstance.data = newData;
  chartInstance.options = getChartOptions(newData);
  chartInstance.update();
};

// Computed property untuk total data bulanan
const monthlyTotals = computed(() => {
  let totalNormal = 0;
  let totalAbnormal = 0;
  let totalWarning = 0;

  Object.values(vehicleDataByMonth.value).forEach((monthData) => {
    if (Array.isArray(monthData) && monthData.length >= 3) {
      totalNormal += monthData[0] || 0;
      totalAbnormal += monthData[1] || 0;
      totalWarning += monthData[2] || 0;
    }
  });

  return {
    normal: totalNormal,
    abnormal: totalAbnormal,
    warning: totalWarning,
  };
});

// Fungsi untuk apply filter
const applyFilter = async () => {
  // Fetch data dengan filter tanggal
  await fetchStatistics();
  await fetchTotalVehicles();
  await fetchMonthlyReports();
  if (selectedVehicleType.value) {
    await fetchVehicleTypeStatus();
  }
};

// Fungsi untuk reset filter
const resetFilter = () => {
  a.value = "";
  u.value = "";
  selectedVehicleType.value = "";

  // Fetch ulang data tanpa filter
  fetchStatistics();
  fetchTotalVehicles();
  fetchMonthlyReports();
};

onMounted(async () => {
  // Fetch data dari backend dulu
  await fetchStatistics(); // Ini akan update pieChartData dan init pie chart
  await fetchTotalVehicles(); // Fetch total vehicles dari unit-pt dan unit-travel
  await fetchVehicleTypes();
  await fetchMonthlyReports(); // Ini akan update vehicleDataByMonth dan call updateChart()

  // Initialize line chart setelah semua data ready
  await nextTick();
  initChart();
  initVehicleTypeChart();
});

// Cleanup chart instances saat component unmount
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
  if (pieChartInstance) {
    pieChartInstance.destroy();
    pieChartInstance = null;
  }
  if (vehicleTypeChartInstance) {
    vehicleTypeChartInstance.destroy();
    vehicleTypeChartInstance = null;
  }
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

        <!-- Konten Utama -->
        <main
          class="bg-[#EFEFEF] flex-1 overflow-y-auto p-1 sm:p-1 md:p-2 lg:p-1"
        >
          <div class="w-full p-2">
            <!-- 6 Konten Sejajar -->
            <div
              class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-1.5 sm:gap-2"
            >
              <!-- Box 1 - Total Vehicles -->
              <div
                @click="
                  openCardDetail('total_vehicles', t('dashboard.totalVehicles'))
                "
                class="bg-white rounded-lg shadow-md p-1.5 sm:p-2 flex items-start gap-1.5 sm:gap-2 min-h-1 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200"
              >
                <UserIcon
                  class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 text-black shrink-0 mt-0.5"
                />
                <div class="flex flex-col flex-1 min-w-0">
                  <p class="text-xs font-regular text-gray-500 truncate">
                    {{ t("dashboard.totalVehicles") }}
                  </p>
                  <h3
                    class="text-sm sm:text-base md:text-lg lg:text-xl font-bold text-black mt-0.5 sm:mt-1"
                  >
                    {{ statisticsData.totalVehicles }}
                  </h3>
                </div>
              </div>

              <!-- Box 2 - Total Normal -->
              <div
                @click="
                  openCardDetail('total_normal', t('dashboard.totalNormal'))
                "
                class="bg-white rounded-lg shadow-md p-1.5 sm:p-2 flex items-start gap-1.5 sm:gap-2 min-h-1 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200"
              >
                <UserIcon
                  class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 text-green-600 shrink-0 mt-0.5"
                />
                <div class="flex flex-col flex-1 min-w-0">
                  <p class="text-xs font-regular text-gray-500 truncate">
                    {{ t("dashboard.totalNormal") }}
                  </p>
                  <h3
                    class="text-sm sm:text-base md:text-lg lg:text-xl font-bold text-green-600 mt-0.5 sm:mt-1"
                  >
                    {{ statisticsData.totalNormal }}
                  </h3>
                </div>
              </div>

              <!-- Box 3 - Total Abnormal -->
              <div
                @click="
                  openCardDetail('total_abnormal', t('dashboard.totalAbnormal'))
                "
                class="bg-white rounded-lg shadow-md p-1.5 sm:p-2 flex items-start gap-1.5 sm:gap-2 min-h-1 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200"
              >
                <UserIcon
                  class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 text-yellow-600 shrink-0 mt-0.5"
                />
                <div class="flex flex-col flex-1 min-w-0">
                  <p class="text-xs font-regular text-gray-500 truncate">
                    {{ t("dashboard.totalAbnormal") }}
                  </p>
                  <h3
                    class="text-sm sm:text-base md:text-lg lg:text-xl font-bold text-yellow-600 mt-0.5 sm:mt-1"
                  >
                    {{ statisticsData.totalAbnormal }}
                  </h3>
                </div>
              </div>

              <!-- Box 4 - Total Warning -->
              <div
                @click="
                  openCardDetail('total_warning', t('dashboard.totalWarning'))
                "
                class="bg-white rounded-lg shadow-md p-1.5 sm:p-2 flex items-start gap-1.5 sm:gap-2 min-h-1 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200"
              >
                <UserIcon
                  class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 text-red-600 shrink-0 mt-0.5"
                />
                <div class="flex flex-col flex-1 min-w-0">
                  <p class="text-xs font-regular text-gray-500 truncate">
                    {{ t("dashboard.totalWarning") }}
                  </p>
                  <h3
                    class="text-sm sm:text-base md:text-lg lg:text-xl font-bold text-red-600 mt-0.5 sm:mt-1"
                  >
                    {{ statisticsData.totalWarning }}
                  </h3>
                </div>
              </div>

              <!-- Box 5 - Total Completed P2H -->
              <div
                @click="
                  openCardDetail(
                    'total_completed',
                    t('dashboard.totalCompletedP2H'),
                  )
                "
                class="bg-white rounded-lg shadow-md p-1.5 sm:p-2 flex items-start gap-1.5 sm:gap-2 min-h-1 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200"
              >
                <UserIcon
                  class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 text-blue-600 shrink-0 mt-0.5"
                />
                <div class="flex flex-col flex-1 min-w-0">
                  <p class="text-xs font-regular text-gray-500 truncate">
                    {{ t("dashboard.totalCompletedP2H") }}
                  </p>
                  <h3
                    class="text-sm sm:text-base md:text-lg lg:text-xl font-bold text-blue-600 mt-0.5 sm:mt-1"
                  >
                    {{ statisticsData.totalCompletedP2H }}
                  </h3>
                </div>
              </div>

              <!-- Box 6 - Total Pending P2H -->
              <div
                @click="
                  openCardDetail(
                    'total_pending',
                    t('dashboard.totalPendingP2H'),
                  )
                "
                class="bg-white rounded-lg shadow-md p-1.5 sm:p-2 flex items-start gap-1.5 sm:gap-2 min-h-1 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200"
              >
                <UserIcon
                  class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 text-gray-600 shrink-0 mt-0.5"
                />
                <div class="flex flex-col flex-1 min-w-0">
                  <p class="text-xs font-regular text-gray-500 truncate">
                    {{ t("dashboard.totalPendingP2H") }}
                  </p>
                  <h3
                    class="text-sm sm:text-base md:text-lg lg:text-xl font-bold text-gray-600 mt-0.5 sm:mt-1"
                  >
                    {{ statisticsData.totalPendingP2H }}
                  </h3>
                </div>
              </div>
            </div>

            <!-- Konten kedua -->
            <div
              class="grid grid-cols-1 lg:grid-cols-2 gap-2 sm:gap-3 md:gap-2 mt-2 sm:mt-3 md:mt-4"
            >
              <div class="flex flex-col w-full gap-2 sm:gap-3">
                <!-- Konten Kiri -->
                <div class="bg-white rounded-lg shadow-md p-3 sm:p-4 md:p-6">
                  <h2
                    class="text-base sm:text-lg md:text-xl font-bold text-gray-800 mb-2 sm:mb-3 md:mb-4"
                  >
                    {{ t("dashboard.filterDay") }}
                  </h2>
                  <div
                    class="grid grid-cols-1 md:grid-cols-2 gap-2 sm:gap-3 mb-3 sm:mb-4"
                  >
                    <div>
                      <label
                        for="filter-start-date"
                        class="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2"
                        >{{ t("dashboard.startDate") }}</label
                      >
                      <input
                        id="filter-start-date"
                        v-model="a"
                        type="date"
                        class="w-full p-1.5 sm:p-2 text-xs sm:text-sm border border-[#C3C3C3] bg-[#ffffff] text-[#777777] rounded-md cursor-pointer focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label
                        for="filter-end-date"
                        class="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2"
                        >{{ t("dashboard.endDate") }}</label
                      >
                      <input
                        id="filter-end-date"
                        v-model="u"
                        type="date"
                        class="w-full p-1.5 sm:p-2 text-xs sm:text-sm border border-[#C3C3C3] bg-[#ffffff] text-[#777777] rounded-md cursor-pointer focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                  <div class="grid grid-cols-2 gap-2 sm:gap-3">
                    <button
                      type="button"
                      @click="applyFilter"
                      class="w-full p-1.5 sm:p-2 bg-indigo-600 text-white text-xs sm:text-sm font-semibold rounded-md hover:bg-indigo-700 transition-colors duration-200"
                    >
                      {{ t("dashboard.applyFilter") }}
                    </button>
                    <button
                      type="button"
                      @click="resetFilter"
                      class="w-full p-1.5 sm:p-2 bg-gray-300 text-gray-700 text-xs sm:text-sm font-semibold rounded-md hover:bg-gray-400 transition-colors duration-200"
                    >
                      {{ t("dashboard.resetFilter") }}
                    </button>
                  </div>
                </div>

                <!-- Tipe kendaraan -->
                <div class="w-full relative">
                  <button
                    @click="isVehicleTypeOpen = !isVehicleTypeOpen"
                    class="w-full bg-white rounded-lg shadow-md p-3 flex items-center justify-between hover:bg-gray-50 transition-colors duration-200"
                  >
                    <p class="text-sm font-semibold text-gray-800">
                      {{ selectedVehicleType || t("dashboard.vehicleType") }}
                    </p>
                    <ChevronDownIcon
                      :class="[
                        'w-5 h-5 text-gray-800 transition-transform duration-200',
                        isVehicleTypeOpen && 'rotate-180',
                      ]"
                    />
                  </button>

                  <!-- Dropdown Menu -->
                  <div
                    v-if="isVehicleTypeOpen"
                    class="absolute top-full left-0 right-0 mt-1 bg-white rounded-lg shadow-lg border border-gray-200 z-10"
                  >
                    <button
                      v-for="type in vehicleTypes"
                      :key="type"
                      @click="
                        selectedVehicleType = type;
                        isVehicleTypeOpen = false;
                      "
                      class="w-full text-left px-4 py-3 hover:bg-indigo-50 transition-colors duration-150 text-sm font-medium text-gray-800 first:rounded-t-lg last:rounded-b-lg"
                    >
                      {{ type }}
                    </button>
                  </div>
                </div>

                <!-- Konten Kiri kedua -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-md font-bold text-gray-800 mb-4">
                      {{ t("dashboard.statusVehicleType") }}
                      {{ selectedVehicleType || t("dashboard.vehicleType") }}
                    </h3>
                    <div class="h-80 w-full">
                      <div
                        v-if="!selectedVehicleType"
                        class="h-full flex items-center justify-center"
                      >
                        <p class="text-gray-400 text-center font-medium">
                          {{ t("dashboard.selectFilter") }}
                        </p>
                      </div>
                      <canvas v-else id="chart-pie-vehicle-type"></canvas>
                    </div>
                  </div>

                  <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-md font-bold text-gray-800 mb-4">
                      {{ t("dashboard.p2hResults") }}
                    </h3>
                    <div class="h-80 w-full">
                      <canvas id="chart-pie-hasil"></canvas>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Konten Tahunan -->
              <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-lg font-bold text-gray-800 mb-2">
                  {{ t("dashboard.p2hAnnualChart") }}
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label
                      for="annual-start-period"
                      class="block text-sm font-medium text-gray-700 mb-2"
                      >{{ t("dashboard.startPeriod") }}</label
                    >
                    <input
                      id="annual-start-period"
                      v-model="annualStartPeriod"
                      type="month"
                      placeholder="Januari 2025"
                      class="w-full p-2 text-sm border border-[#C3C3C3] bg-[#ffffff] text-[#777777] rounded-md cursor-pointer"
                    />
                  </div>
                  <div>
                    <label
                      for="annual-end-period"
                      class="block text-sm font-medium text-gray-700 mb-2"
                      >{{ t("dashboard.endPeriod") }}</label
                    >
                    <input
                      id="annual-end-period"
                      v-model="annualEndPeriod"
                      type="month"
                      placeholder="Januari 2026"
                      class="w-full p-2 text-sm border border-[#C3C3C3] bg-[#ffffff] text-[#777777] rounded-md cursor-pointer"
                    />
                  </div>
                </div>

                <!-- Grafik tahunan -->
                <div class="mt-5">
                  <div
                    class="w-full bg-linear-to-br h-full from-gray-100 to-gray-50 rounded-lg border border-gray-200 shadow-lg p-6 hover:shadow-xl transition-shadow duration-300"
                  >
                    <div class="flex items-center justify-between mb-6">
                      <div>
                        <h6 class="text-gray-900 font-bold text-lg">
                          {{ t("dashboard.vehicleStatusMonthly") }}
                        </h6>
                      </div>
                    </div>
                    <div class="w-full h-80 relative">
                      <canvas id="chart-vehicles"></canvas>
                    </div>
                    <div
                      class="flex gap-1 pt-6 border-t border-gray-200 justify-center"
                    >
                      <div class="text-center">
                        <div
                          class="flex items-center justify-center gap-2 mb-2"
                        >
                          <div class="w-3 h-3 rounded-full bg-green-500"></div>
                          <span
                            class="text-xs mr-3 font-semibold text-gray-600"
                            >{{ t("dashboard.normal") }}</span
                          >
                        </div>
                        <p class="text-xl font-bold text-green-600">
                          {{ monthlyTotals.normal }}
                        </p>
                      </div>
                      <div class="text-center">
                        <div
                          class="flex items-center justify-center gap-2 mb-2"
                        >
                          <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                          <span
                            class="text-xs mr-3 font-semibold text-gray-600"
                            >{{ t("dashboard.abnormal") }}</span
                          >
                        </div>
                        <p class="text-xl font-bold text-yellow-600">
                          {{ monthlyTotals.abnormal }}
                        </p>
                      </div>
                      <div class="text-center">
                        <div
                          class="flex items-center justify-center gap-2 mb-2"
                        >
                          <div class="w-3 h-3 rounded-full bg-red-500"></div>
                          <span class="text-xs font-semibold text-gray-600">{{
                            t("dashboard.warning")
                          }}</span>
                        </div>
                        <p class="text-xl font-bold text-red-600">
                          {{ monthlyTotals.warning }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- Card Detail Modal -->
    <CardDetailModal
      :isOpen="modalOpen"
      :cardType="modalCardType"
      :cardTitle="modalCardTitle"
      :items="modalItems"
      :loading="modalLoading"
      @close="closeModal"
    />
  </div>
</template>
