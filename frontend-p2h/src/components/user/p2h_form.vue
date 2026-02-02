<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import NavBar from "../bar/header-user.vue";
import Footer from "../bar/footer.vue";
import {
  InformationCircleIcon,
  MagnifyingGlassIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ChevronDownIcon,
} from "@heroicons/vue/24/solid";
import { api } from "../../services/api";

const router = useRouter();

// --- STATE MANAGEMENT ---
const searchInput = ref("");
const vehicleData = ref(null);
const p2hStatus = ref(null);
const isAuthenticated = ref(false);
const questions = ref([]);
const answers = ref({});
const loading = ref(false);
const isSubmitting = ref(false);

// State Metadata (Shift & Durasi)
const selectedShift = ref("");
const selectedDuration = ref("");
const currentShiftInfo = ref(null); // Info shift dari backend
const shiftWarning = ref(""); // Peringatan jika pilih shift salah

// User data for welcome message
const userData = ref({
  full_name: "User",
});
const isLoadingUserName = ref(true); // Track loading state untuk nama user

// --- LOGIKA BUSINESS ---

// Fetch user profile for welcome message
const fetchUserProfile = async () => {
  // Only fetch if user is authenticated
  if (!isAuthenticated.value) {
    userData.value.full_name = "User";
    isLoadingUserName.value = false;
    return;
  }

  try {
    const response = await api.get("/users/me");
    console.log("✅ User profile fetched:", response.data.payload);
    userData.value.full_name = response.data.payload.full_name || "User";
  } catch (error) {
    console.error("❌ Gagal fetch user profile:", error);
    // Keep default name if fetch fails
    userData.value.full_name = "User";
  } finally {
    isLoadingUserName.value = false;
  }
};

const checkAuthentication = () => {
  const token = localStorage.getItem("access_token");
  isAuthenticated.value = !!token;
};

const fetchCurrentShift = async () => {
  try {
    const response = await api.get("/p2h/current-shift");
    currentShiftInfo.value = response.data.payload;
    // Auto-select shift sesuai waktu sekarang
    selectedShift.value = currentShiftInfo.value.current_shift.toString();
  } catch (error) {
    console.error("❌ Gagal mendapatkan info shift:", error);
  } finally {
    // Cleanup if needed
  }
};

const validateShiftTime = () => {
  if (!currentShiftInfo.value || !selectedShift.value) return true;

  const selected = selectedShift.value;
  const currentTime = new Date();
  const hour = currentTime.getHours();

  // Validasi berdasarkan shift yang dipilih
  if (selected === "non-shift" || selected === "0") {
    // Non-Shift: 00:00 - 16:00
    if (hour >= 16) {
      shiftWarning.value = `⚠️ Non-Shift hanya bisa diisi sebelum jam 16:00. Waktu sekarang: ${currentTime.toLocaleTimeString('id-ID', {hour: '2-digit', minute: '2-digit'})}`;
      return false;
    }
  } else if (selected === "long-shift-1" || selected === "11") {
    // Long Shift 1: 06:00 - 19:00
    if (hour < 6 || hour >= 19) {
      shiftWarning.value = `⚠️ Long Shift 1 hanya bisa diisi pada jam 06:00-19:00. Waktu sekarang: ${currentTime.toLocaleTimeString('id-ID', {hour: '2-digit', minute: '2-digit'})}`;
      return false;
    }
  } else if (selected === "long-shift-2" || selected === "12") {
    // Long Shift 2: 18:00 - 07:00 (melewati midnight)
    if (hour < 18 && hour >= 7) {
      shiftWarning.value = `⚠️ Long Shift 2 hanya bisa diisi pada jam 18:00-07:00. Waktu sekarang: ${currentTime.toLocaleTimeString('id-ID', {hour: '2-digit', minute: '2-digit'})}`;
      return false;
    }
  } else {
    // Regular shift validation
    const selectedShiftNum = parseInt(selected);
    
    // Shift 1: 06:00 - 15:00
    if (selectedShiftNum === 1 && (hour < 6 || hour >= 15)) {
      shiftWarning.value = `⚠️ Shift 1 hanya bisa diisi pada jam 06:00-15:00. Waktu sekarang: ${currentTime.toLocaleTimeString('id-ID', {hour: '2-digit', minute: '2-digit'})}`;
      return false;
    }
    
    // Shift 2: 14:00 - 23:00
    if (selectedShiftNum === 2 && (hour < 14 || hour >= 23)) {
      shiftWarning.value = `⚠️ Shift 2 hanya bisa diisi pada jam 14:00-23:00. Waktu sekarang: ${currentTime.toLocaleTimeString('id-ID', {hour: '2-digit', minute: '2-digit'})}`;
      return false;
    }
    
    // Shift 3: 22:00 - 07:00 (melewati midnight)
    if (selectedShiftNum === 3 && (hour < 22 && hour >= 7)) {
      shiftWarning.value = `⚠️ Shift 3 hanya bisa diisi pada jam 22:00-07:00. Waktu sekarang: ${currentTime.toLocaleTimeString('id-ID', {hour: '2-digit', minute: '2-digit'})}`;
      return false;
    }
  }

  shiftWarning.value = "";
  return true;
};

const handleLoginRedirect = () => {
  alert(
    "Kendaraan belum di-P2H. Silakan login terlebih dahulu untuk mengisi form P2H.",
  );
  router.push("/login");
};

const handleSearchVehicle = async () => {
  if (!searchInput.value) return;
  checkAuthentication();

  try {
    loading.value = true;
    const response = await api.get(`/vehicles/lambung/${searchInput.value}`);

    vehicleData.value = response.data.payload.vehicle;
    p2hStatus.value = {
      color: response.data.payload.color_code,
      completed: response.data.payload.p2h_completed_today,
      status: response.data.payload.status_p2h,
      canSubmit: response.data.payload.can_submit_p2h,
      message: response.data.payload.message,
      currentShift: response.data.payload.current_shift,
      shiftsCompleted: response.data.payload.shifts_completed,
    };

    // Cek apakah shift SAAT INI sudah diisi
    const currentShiftDone = p2hStatus.value.shiftsCompleted.includes(
      p2hStatus.value.currentShift,
    );

    // Jika shift saat ini sudah diisi atau tidak bisa submit, jangan tampilkan form
    if (currentShiftDone || !p2hStatus.value.canSubmit) {
      questions.value = [];
      return;
    }

    // ✅ Kalau sampai sini = canSubmit = true, user authenticated → fetch checklist
    if (isAuthenticated.value && p2hStatus.value.canSubmit) {
      await fetchChecklist(vehicleData.value.vehicle_type);
    } else {
      questions.value = [];
    }
  } catch (error) {
    alert(error.response?.data?.detail || "Nomor lambung tidak ditemukan");
    vehicleData.value = null;
    p2hStatus.value = null;
    questions.value = [];
  } finally {
    loading.value = false;
  }
};

const fetchChecklist = async (vehicleType) => {
  try {
    console.log("🔍 [DEBUG] Fetching checklist for vehicle type:", vehicleType);
    const response = await api.get("/p2h/checklist-items");
    const allQuestions = response.data.payload;
    console.log("📋 [DEBUG] Total questions from API:", allQuestions.length);

    questions.value = allQuestions.filter(
      (q) => q.vehicle_tags && q.vehicle_tags.includes(vehicleType),
    );
    console.log("✅ [DEBUG] Questions after filter:", questions.value.length);
    console.log("📝 [DEBUG] Filtered questions:", questions.value);

    questions.value = questions.value.map((q) => ({
      ...q,
      pertanyaan: q.item_name,
      // Parse options: format "Text yang ditampilkan|Status"
      parsedOptions: q.options.map((opt) => {
        if (opt.includes("|")) {
          const [displayText, status] = opt.split("|");
          return { displayText: displayText.trim(), status: status.trim() };
        }
        // Fallback jika tidak ada separator
        return { displayText: opt, status: "Normal" };
      }),
    }));

    questions.value.forEach((q) => {
      answers.value[q.id] = { status: "Normal", keterangan: "" };
    });
  } catch (error) {
    console.error("❌ Gagal memuat checklist", error);
  } finally {
    // Cleanup if needed
  }
};

const handleSubmitReport = async () => {
  if (!vehicleData.value) return;

  // Validasi Shift Time Real-time
  if (!validateShiftTime()) {
    alert(shiftWarning.value);
    return;
  }

  // Validasi Dropdown Mandatory (untuk informasi user, tapi tidak dikirim ke backend)
  if (!selectedShift.value || !selectedDuration.value) {
    alert("Harap pilih Shift dan Durasi Pemakaian terlebih dahulu!");
    return;
  }

  // Validasi Checklist
  for (const qId in answers.value) {
    const ans = answers.value[qId];
    if (
      (ans.status === "Abnormal" || ans.status === "Warning") &&
      !ans.keterangan.trim()
    ) {
      alert(`Harap isi keterangan untuk item yang bermasalah!`);
      return;
    }
  }

  try {
    isSubmitting.value = true;

    // Backend auto-detect shift berdasarkan waktu submit
    // shift_number dan duration hanya untuk informasi user, tidak dikirim
    const payload = {
      vehicle_id: vehicleData.value.id,
      details: Object.keys(answers.value).map((id) => ({
        checklist_item_id: id,
        status: answers.value[id].status.toLowerCase(), // Convert ke lowercase untuk backend
        keterangan: answers.value[id].keterangan,
      })),
    };

    console.log("📤 Payload yang dikirim:", JSON.stringify(payload, null, 2));
    const response = await api.post("/p2h/submit", payload);

    // Hitung overall status dari jawaban
    let hasWarning = false;
    let hasAbnormal = false;

    for (const qId in answers.value) {
      const status = answers.value[qId].status;
      if (status === "Warning") {
        hasWarning = true;
        break; // Warning is highest priority
      } else if (status === "Abnormal") {
        hasAbnormal = true;
      }
    }

    // Determine overall status
    let overallStatus = "normal";
    if (hasWarning) {
      overallStatus = "warning";
    } else if (hasAbnormal) {
      overallStatus = "abnormal";
    }

    // Simpan data ke sessionStorage untuk ditampilkan di halaman hasil
    const resultData = {
      status: overallStatus,
      vehicleData: vehicleData.value,
      submissionTime: new Date().toLocaleString("id-ID"),
    };
    sessionStorage.setItem("p2hResult", JSON.stringify(resultData));

    // Redirect ke halaman hasil
    router.push({ name: "hasil-form" });
  } catch (error) {
    console.error("❌ Submit error:", error.response?.data);
    alert(
      "Error: " + (error.response?.data?.detail || "Gagal mengirim laporan"),
    );
  } finally {
    isSubmitting.value = false;
  }
};

const groupedQuestions = computed(() => {
  return questions.value.reduce((acc, obj) => {
    const key = obj.section_name;
    if (!acc[key]) acc[key] = [];
    acc[key].push(obj);
    return acc;
  }, {});
});

// Helper styling untuk Radio Button sesuai Status
const getOptionClass = (id, opt) => {
  const currentStatus = answers.value[id]?.status;
  if (currentStatus !== opt) return "bg-zinc-50 border-zinc-200 opacity-60";

  if (opt === "Normal")
    return "bg-green-100 border-green-400 ring-1 ring-green-400 opacity-100";
  if (opt === "Abnormal")
    return "bg-yellow-100 border-yellow-400 ring-1 ring-yellow-400 opacity-100";
  if (opt === "Warning")
    return "bg-red-100 border-red-400 ring-1 ring-red-400 opacity-100";
  return "bg-zinc-50 border-zinc-200";
};

onMounted(() => {
  checkAuthentication();
  fetchCurrentShift(); // Fetch shift info saat component dimount
  fetchUserProfile(); // Fetch user profile untuk welcome message
});
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat'] bg-zinc-50">
    <NavBar />

    <main
      class="flex-1 flex flex-col items-center bg-zinc-100 px-4 pt-24 pb-45 md:pb-30 bg-cover bg-fixed bg-center"
      style="background-image: url(&quot;/image_asset/BG_2.png&quot;)"
    >
      <div class="w-full max-w-4xl space-y-4">
        <div class="p-8 bg-white rounded-2xl shadow-sm border border-zinc-200">
          <h1 class="text-2xl font-extrabold mb-2 text-zinc-900 leading-tight">
            <template v-if="isLoadingUserName">
              Selamat datang...
            </template>
            <template v-else>
              Selamat datang {{ userData.full_name }}
            </template>
          </h1>
          <p class="text-zinc-600 text-sm leading-relaxed">
            Mohon mengisi informasi keadaan kendaraan hari ini sebelum anda
            bekerja atau sebelum memakai kendaraan di area PT Indominco Mandiri.
          </p>
        </div>

        <div
          class="p-8 bg-white rounded-2xl shadow-sm border border-zinc-200 space-y-4"
        >
          <h2 class="text-lg font-bold text-zinc-800">
            Informasi kondisi kerusakan pada kendaraan pada keterangan dibawah :
          </h2>

          <div
            class="flex items-start gap-2 p-3 bg-red-50 rounded-lg text-xs border border-red-100"
          >
            <InformationCircleIcon
              class="h-4 w-4 text-red-500 shrink-0 mt-0.5"
            />
            <p class="text-red-700 leading-relaxed font-medium">
              Jika memilih status
              <span class="font-bold text-red-600">Abnormal</span> atau
              <span class="font-bold text-red-600">Warning</span>, pengguna
              wajib mengisi keterangan kerusakan sebagai informasi tambahan.
            </p>
          </div>

          <div class="space-y-4 pt-2">
            <div>
              <span
                class="px-4 py-1.5 bg-green-200 text-green-900 rounded-full text-base font-black tracking-wide"
                >NORMAL</span
              >
              <p class="text-zinc-500 text-xs mt-2 font-medium italic">
                Bagian kendaraan dalam kondisi baik dan berfungsi normal tanpa
                ditemukan kerusakan.
              </p>
            </div>
            <div>
              <span
                class="px-4 py-1.5 bg-yellow-200 text-yellow-900 rounded-full text-sm font-black tracking-wide"
                >ABNORMAL</span
              >
              <p class="text-zinc-500 text-xs mt-2 font-medium italic">
                Bagian kendaraan terdapat kerusakan ringan, namun masih dapat
                digunakan dan perlu dilakukan pemeriksaan atau perbaikan di
                bengkel.
              </p>
            </div>
            <div>
              <span
                class="px-4 py-1.5 bg-red-200 text-red-900 rounded-full text-sm font-black tracking-wide"
                >WARNING</span
              >
              <p class="text-zinc-500 text-xs mt-2 font-medium italic">
                Bagian kendaraan mengalami kerusakan serius, tidak dapat
                digunakan dan harus segera dibawa ke bengkel untuk penanganan
                lebih lanjut.
              </p>
            </div>
          </div>
        </div>

        <div class="flex flex-col gap-4 font-bold">
          <!-- Info Waktu Real-Time -->
          <div
            v-if="currentShiftInfo"
            class="p-4 bg-blue-50 border-2 border-blue-300 rounded-2xl"
          >
            <div class="flex items-center gap-2 text-blue-900">
              <InformationCircleIcon class="h-5 w-5" />
              <p class="text-sm font-bold">
                Waktu Sekarang:
                <span class="font-extrabold">{{
                  currentShiftInfo.current_time
                }}</span>
                - {{ currentShiftInfo.shift_info.name }} ({{
                  currentShiftInfo.shift_info.time_range
                }})
              </p>
            </div>
            <p class="text-xs text-blue-700 mt-1 font-semibold">
              Toleransi pengisian: 1 jam sebelum shift (mulai
              {{ currentShiftInfo.shift_info.tolerance_start }})
            </p>
          </div>

          <!-- Warning jika pilih shift yang salah -->
          <div
            v-if="shiftWarning"
            class="p-4 bg-red-50 border-2 border-red-400 rounded-2xl"
          >
            <div class="flex items-center gap-2 text-red-900">
              <ExclamationTriangleIcon class="h-5 w-5" />
              <p class="text-sm font-bold">{{ shiftWarning }}</p>
            </div>
          </div>

          <div
            class="p-6 bg-white rounded-2xl shadow-sm border border-zinc-200"
          >
            <label class="block text-base mb-3 text-zinc-900"
              >Apakah anda kerja Shift / Non-Shift</label
            >
            <div class="relative">
              <select
                v-model="selectedShift"
                @change="validateShiftTime"
                class="w-full p-3.5 bg-white border-2 border-zinc-300 rounded-xl appearance-none outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-sm font-semibold text-zinc-900 cursor-pointer hover:border-purple-400 transition-colors"
              >
                <option value="" disabled class="text-zinc-500">
                  Pilih Shift
                </option>
                <option value="1" class="text-zinc-900">
                  Shift 1 (07:00 - 15:00)
                </option>
                <option value="2" class="text-zinc-900">
                  Shift 2 (15:00 - 23:00)
                </option>
                <option value="3" class="text-zinc-900">
                  Shift 3 (23:00 - 07:00)
                </option>
                <option value="non-shift" class="text-zinc-900">
                  Non Shift (07:00 - 15:00)
                </option>
                <option value="long-shift-1" class="text-zinc-900">
                  Long Shift 1 (07:00 - 00:00)
                </option>
                <option value="long-shift-2" class="text-zinc-900">
                  Long Shift 2 (00:00 - 07:00)
                </option>
              </select>
              <ChevronDownIcon
                class="h-5 w-5 absolute right-4 top-1/2 -translate-y-1/2 text-purple-600 pointer-events-none"
              />
            </div>
          </div>
          <div
            class="p-6 bg-white rounded-2xl shadow-sm border border-zinc-200"
          >
            <label class="block text-base mb-3 text-zinc-900"
              >Rencana durasi pemakaian kendaraan</label
            >
            <div class="relative">
              <select
                v-model="selectedDuration"
                class="w-full p-3.5 bg-white border-2 border-zinc-300 rounded-xl appearance-none outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-sm font-semibold text-zinc-900 cursor-pointer hover:border-purple-400 transition-colors"
              >
                <option value="" disabled selected class="text-zinc-500">
                  Pilih Durasi
                </option>
                <option value="<8h" class="text-zinc-900">&lt;8 Jam</option>
                <option value="8h" class="text-zinc-900">8 Jam</option>
                <option value=">8h" class="text-zinc-900">&gt;8 Jam</option>
              </select>
              <ChevronDownIcon
                class="h-5 w-5 absolute right-4 top-1/2 -translate-y-1/2 text-purple-600 pointer-events-none"
              />
            </div>
          </div>
        </div>

        <div
          class="p-8 bg-white rounded-2xl shadow-sm border border-zinc-200 space-y-4"
        >
          <h2
            class="text-lg font-extrabold border-b-3 border-purple-600 inline-block pb-1 text-zinc-900"
          >
            Jenis Kendaraan
          </h2>
          <div class="space-y-2">
            <div class="flex gap-2">
              <input
                v-model="searchInput"
                @keyup.enter="handleSearchVehicle"
                placeholder="Cari nomor lambung"
                class="text-sm flex-1 p-3 bg-white border-2 border-zinc-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none font-semibold text-zinc-900 placeholder-zinc-400"
              />
              <button
                @click="handleSearchVehicle"
                class="bg-purple-600 hover:bg-purple-700 text-white px-8 rounded-xl font-bold flex items-center gap-2 transition-all shadow-md active:scale-95"
              >
                Cari <MagnifyingGlassIcon class="h-5 w-5" />
              </button>
            </div>
          </div>

          <div
            v-if="vehicleData"
            :class="[
              'p-6 rounded-2xl border-2 transition-all',
              p2hStatus?.color === 'green'
                ? 'bg-green-50 border-green-400'
                : p2hStatus?.color === 'yellow'
                  ? 'bg-yellow-50 border-yellow-400'
                  : 'bg-red-50 border-red-400',
            ]"
          >
            <div class="space-y-2">
              <p
                class="text-sm font-bold"
                :class="
                  p2hStatus?.color === 'green'
                    ? 'text-green-900'
                    : p2hStatus?.color === 'yellow'
                      ? 'text-yellow-900'
                      : 'text-red-900'
                "
              >
                Nomor lambung :
                <span class="font-semibold text-zinc-800">{{
                  vehicleData.no_lambung
                }}</span>
              </p>
              <p
                class="text-sm font-bold"
                :class="
                  p2hStatus?.color === 'green'
                    ? 'text-green-900'
                    : p2hStatus?.color === 'yellow'
                      ? 'text-yellow-900'
                      : 'text-red-900'
                "
              >
                Warna nomor lambung :
                <span class="font-semibold text-zinc-800">{{
                  vehicleData.warna_no_lambung || "-"
                }}</span>
              </p>
              <p
                class="text-sm font-bold"
                :class="
                  p2hStatus?.color === 'green'
                    ? 'text-green-900'
                    : p2hStatus?.color === 'yellow'
                      ? 'text-yellow-900'
                      : 'text-red-900'
                "
              >
                Lokasi Kendaraan :
                <span class="font-semibold text-zinc-800">{{
                  vehicleData.lokasi_kendaraan || "-"
                }}</span>
              </p>
              <p
                class="text-sm font-bold"
                :class="
                  p2hStatus?.color === 'green'
                    ? 'text-green-900'
                    : p2hStatus?.color === 'yellow'
                      ? 'text-yellow-900'
                      : 'text-red-900'
                "
              >
                Merek Kendaraan :
                <span class="font-semibold text-zinc-800">{{
                  vehicleData.merk
                }}</span>
              </p>
              <p
                class="text-sm font-bold"
                :class="
                  p2hStatus?.color === 'green'
                    ? 'text-green-900'
                    : p2hStatus?.color === 'yellow'
                      ? 'text-yellow-900'
                      : 'text-red-900'
                "
              >
                Tipe Kendaraan :
                <span class="font-semibold text-zinc-800">{{
                  vehicleData.vehicle_type
                }}</span>
              </p>
              <p
                class="text-sm font-bold"
                :class="
                  p2hStatus?.color === 'green'
                    ? 'text-green-900'
                    : p2hStatus?.color === 'yellow'
                      ? 'text-yellow-900'
                      : 'text-red-900'
                "
              >
                Plat Kendaraan :
                <span class="font-semibold text-zinc-800">{{
                  vehicleData.plat_nomor
                }}</span>
              </p>
              <div
                class="mt-2 pt-2 border-t-2"
                :class="
                  p2hStatus?.color === 'green'
                    ? 'border-green-200'
                    : p2hStatus?.color === 'yellow'
                      ? 'border-yellow-200'
                      : 'border-red-200'
                "
              >
                <p
                  class="text-sm font-extrabold"
                  :class="
                    p2hStatus?.color === 'green'
                      ? 'text-green-900'
                      : p2hStatus?.color === 'yellow'
                        ? 'text-yellow-900'
                        : 'text-red-900'
                  "
                >
                  Status P2H:
                  <span class="font-extrabold">{{
                    p2hStatus?.message || p2hStatus?.status
                  }}</span>
                </p>
                <p
                  v-if="
                    p2hStatus?.shiftsCompleted &&
                    p2hStatus.shiftsCompleted.length > 0
                  "
                  class="text-xs mt-1"
                  :class="
                    p2hStatus?.color === 'green'
                      ? 'text-green-700'
                      : p2hStatus?.color === 'yellow'
                        ? 'text-yellow-700'
                        : 'text-red-700'
                  "
                >
                  Shift yang sudah di-P2H: Shift
                  {{ p2hStatus.shiftsCompleted.join(", Shift ") }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <section
          v-if="
            p2hStatus?.color !== 'green' &&
            isAuthenticated &&
            questions.length > 0
          "
          class="space-y-6 pb-10"
        >
          <div
            v-for="(items, section) in groupedQuestions"
            :key="section"
            class="p-8 bg-white rounded-2xl shadow-sm border border-zinc-200 space-y-2"
          >
            <h3
              class="text-lg font-extrabold text-zinc-900 border-b-2 border-zinc-100 pb-3"
            >
              {{ vehicleData?.vehicle_type || section }}
            </h3>

            <div v-for="q in items" :key="q.id" class="space-y-2">
              <p class="font-bold text-zinc-800 text-base">
                {{ q.pertanyaan }}
              </p>

              <div class="grid grid-cols-1 gap-2.5">
                <label
                  v-for="opt in q.parsedOptions"
                  :key="opt.status"
                  :class="[
                    'flex items-center p-4 rounded-xl  cursor-pointer transition-all duration-200',
                    getOptionClass(q.id, opt.status),
                  ]"
                >
                  <input
                    type="radio"
                    v-model="answers[q.id].status"
                    :value="opt.status"
                    class="hidden"
                  />

                  <div
                    :class="[
                      'w-5 h-5 rounded-full border-2 flex items-center justify-center mr-4 transition-colors',
                      answers[q.id].status === opt.status
                        ? 'border-purple-600 bg-white'
                        : 'border-zinc-400',
                    ]"
                  >
                    <div
                      v-if="answers[q.id].status === opt.status"
                      class="w-3 h-3 bg-purple-600 rounded-full animate-pulse"
                    ></div>
                  </div>

                  <span class="font-bold text-sm tracking-wide text-zinc-900">{{
                    opt.displayText
                  }}</span>
                </label>
              </div>

              <div
                v-if="answers[q.id].status !== 'Normal'"
                class="mt-4 space-y-2"
              >
                <textarea
                  v-model="answers[q.id].keterangan"
                  placeholder="Keterangan kerusakan"
                  class="w-full p-4 bg-white border-2 border-zinc-300 rounded-xl text-sm font-semibold text-zinc-900 placeholder-zinc-400 focus:ring-2 focus:ring-red-400 focus:border-red-400 outline-none"
                  rows="3"
                ></textarea>
                <div
                  class="flex items-center gap-1.5 text-[10px] text-red-500 font-bold italic"
                >
                  <ExclamationTriangleIcon class="h-3 w-3" /> HARAP ISI
                  KETERANGAN KERUSAKAN
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-end">
            <button
              @click="handleSubmitReport"
              :disabled="isSubmitting"
              class="px-10 sm:px-10 py-2.5 sm:py-3 bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs sm:text-sm rounded-lg shadow-md transition-all active:scale-95 disabled:bg-zinc-400 disabled:shadow-sm flex items-center justify-center w-auto sm:w-auto"
            >
              {{ isSubmitting ? "MENGIRIM..." : "Kirim" }}
            </button>
          </div>
        </section>
      </div>
    </main>
    <Footer />
  </div>
</template>

<style scoped>
label {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

select {
  cursor: pointer;
}

/* Responsivitas font jika layar sangat kecil */
@media (max-width: 640px) {
  h1 {
    font-size: 1.25rem;
  }
  .p-8 {
    padding: 1.5rem;
  }
}
</style>
