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
import { STORAGE_KEYS } from "../../constants";

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
  // Check localStorage first for cached user data
  const cachedUserData = localStorage.getItem("user_data");
  if (cachedUserData) {
    try {
      const parsed = JSON.parse(cachedUserData);
      if (parsed.full_name) {
        userData.value.full_name = parsed.full_name;
        isLoadingUserName.value = false;
        return;
      }
    } catch (e) {
      console.error("Error parsing cached user data:", e);
    }
  }

  // Check if authenticated before making API call
  const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
  if (!token) {
    userData.value.full_name = "User";
    isLoadingUserName.value = false;
    return;
  }

  try {
    const response = await api.get("/users/me");
    userData.value.full_name = response.data.payload.full_name || "User";
  } catch (error) {
    console.error("Gagal fetch user profile:", error);
    // Keep default name if fetch fails
    userData.value.full_name = "User";
  } finally {
    isLoadingUserName.value = false;
  }
};

const checkAuthentication = () => {
  const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
  isAuthenticated.value = !!token;
  console.log(
    "🔐 [AUTH] Token ada:",
    !!token,
    token ? `(${token.substring(0, 20)}...)` : "(null)",
  );
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
      shiftWarning.value = `⚠️ Non-Shift hanya bisa diisi sebelum jam 16:00. Waktu sekarang: ${currentTime.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" })}`;
      return false;
    }
  } else if (selected === "long-shift-1" || selected === "11") {
    // Long Shift 1: 06:00 - 19:00
    if (hour < 6 || hour >= 19) {
      shiftWarning.value = `⚠️ Long Shift 1 hanya bisa diisi pada jam 06:00-19:00. Waktu sekarang: ${currentTime.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" })}`;
      return false;
    }
  } else if (selected === "long-shift-2" || selected === "12") {
    // Long Shift 2: 18:00 - 07:00 (melewati midnight)
    if (hour < 18 && hour >= 7) {
      shiftWarning.value = `⚠️ Long Shift 2 hanya bisa diisi pada jam 18:00-07:00. Waktu sekarang: ${currentTime.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" })}`;
      return false;
    }
  } else {
    // Regular shift validation
    const selectedShiftNum = parseInt(selected);

    // Shift 1: 06:00 - 15:00
    if (selectedShiftNum === 1 && (hour < 6 || hour >= 15)) {
      shiftWarning.value = `⚠️ Shift 1 hanya bisa diisi pada jam 06:00-15:00. Waktu sekarang: ${currentTime.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" })}`;
      return false;
    }

    // Shift 2: 14:00 - 23:00
    if (selectedShiftNum === 2 && (hour < 14 || hour >= 23)) {
      shiftWarning.value = `⚠️ Shift 2 hanya bisa diisi pada jam 14:00-23:00. Waktu sekarang: ${currentTime.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" })}`;
      return false;
    }

    // Shift 3: 22:00 - 07:00 (melewati midnight)
    if (selectedShiftNum === 3 && hour < 22 && hour >= 7) {
      shiftWarning.value = `⚠️ Shift 3 hanya bisa diisi pada jam 22:00-07:00. Waktu sekarang: ${currentTime.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" })}`;
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
  
  // Validasi minimal 2 karakter untuk search
  if (searchInput.value.trim().length < 2) {
    alert("Minimal 2 karakter untuk pencarian");
    return;
  }
  
  checkAuthentication();

  try {
    loading.value = true;
    const response = await api.get(`/vehicles/lambung/${searchInput.value.trim()}`);

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

    console.log("🔍 [P2H DEBUG] === DETAILED DEBUG INFO ===");
    console.log("🔍 [P2H DEBUG] currentShiftDone:", currentShiftDone);
    console.log("🔍 [P2H DEBUG] canSubmit:", p2hStatus.value.canSubmit);
    console.log("🔍 [P2H DEBUG] isAuthenticated:", isAuthenticated.value);
    console.log("🔍 [P2H DEBUG] vehicle_type:", vehicleData.value.vehicle_type);
    console.log("🔍 [P2H DEBUG] currentShift:", p2hStatus.value.currentShift);
    console.log("🔍 [P2H DEBUG] shiftsCompleted:", p2hStatus.value.shiftsCompleted);
    console.log("🔍 [P2H DEBUG] color:", p2hStatus.value.color);
    console.log("🔍 [P2H DEBUG] status:", p2hStatus.value.status);
    console.log("🔍 [P2H DEBUG] message:", p2hStatus.value.message);
    console.log("🔍 [P2H DEBUG] p2hStatus full object:", p2hStatus.value);
    console.log("🔍 [P2H DEBUG] === END DEBUG INFO ===");

    // Special handling untuk Travel atau Light Vehicle
    const isTravel = vehicleData.value.vehicle_type?.toLowerCase().includes('travel') ||
                    vehicleData.value.vehicle_type?.toLowerCase().includes('light vehicle');

    // Jika shift saat ini sudah diisi, jangan tampilkan form
    // KECUALI untuk Travel yang mungkin punya aturan khusus
    if ((currentShiftDone || !p2hStatus.value.canSubmit) && !isTravel) {
      console.log(
        "❌ [P2H DEBUG] Tidak fetch checklist - shift done atau tidak bisa submit",
        "Reason: currentShiftDone =", currentShiftDone, ", canSubmit =", p2hStatus.value.canSubmit
      );
      questions.value = [];
      return;
    }

    // Untuk Travel, coba fetch checklist meskipun ada pembatasan
    if (isTravel && !isAuthenticated.value) {
      console.log("❌ [P2H DEBUG] Travel tidak authenticated");
      questions.value = [];
      return;
    }

    if (isAuthenticated.value) {
      console.log("✅ [P2H DEBUG] Fetching checklist for:", vehicleData.value.vehicle_type);
      console.log("✅ [P2H DEBUG] isTravel:", isTravel);
      console.log("✅ [P2H DEBUG] Will skip restrictions for Travel:", isTravel && (currentShiftDone || !p2hStatus.value.canSubmit));
      await fetchChecklist(vehicleData.value.vehicle_type);
    } else {
      console.log("❌ [P2H DEBUG] User tidak authenticated");
      questions.value = [];
    }
  } catch (error) {
    console.error("❌ [Search Error]", error);
    const errorMsg = error.response?.data?.detail || "Nomor lambung/polisi tidak ditemukan";
    alert(`${errorMsg}\n\nPastikan:\n✓ Format benar (contoh: P.309 atau KT1234AB)\n✓ Kendaraan sudah terdaftar di sistem\n✓ Minimal 2 karakter untuk pencarian`);
    vehicleData.value = null;
    p2hStatus.value = null;
    questions.value = [];
  } finally {
    loading.value = false;
  }
};

const forceFetchChecklist = async () => {
  if (!vehicleData.value) {
    alert("Tidak ada data kendaraan. Silakan cari kendaraan terlebih dahulu.");
    return;
  }

  console.log("🔧 [FORCE FETCH] Mencoba fetch checklist secara paksa...");
  console.log("🔧 [FORCE FETCH] Vehicle Type:", vehicleData.value.vehicle_type);
  console.log("🔧 [FORCE FETCH] Is Authenticated:", isAuthenticated.value);

  if (!isAuthenticated.value) {
    alert("Anda belum login. Silakan login terlebih dahulu.");
    return;
  }

  try {
    loading.value = true;
    await fetchChecklist(vehicleData.value.vehicle_type);
    console.log("🔧 [FORCE FETCH] Berhasil fetch", questions.value.length, "questions");
    
    if (questions.value.length === 0) {
      alert(`⚠️ Tidak ada checklist untuk tipe kendaraan '${vehicleData.value.vehicle_type}'. Silakan hubungi admin.`);
    } else {
      alert(`✅ Berhasil memuat ${questions.value.length} item checklist untuk ${vehicleData.value.vehicle_type}`);
    }
  } catch (error) {
    console.error("🔧 [FORCE FETCH] Error:", error);
    alert("❌ Gagal memuat checklist: " + (error.response?.data?.detail || error.message));
  } finally {
    loading.value = false;
  }
};

const debugAnswers = () => {
  console.log("🔍 [DEBUG ANSWERS] Current answers state:");
  console.log("🔍 [DEBUG ANSWERS] answers.value:", answers.value);
  console.log("🔍 [DEBUG ANSWERS] answers keys:", Object.keys(answers.value));
  console.log("🔍 [DEBUG ANSWERS] answers entries:", Object.entries(answers.value));
  
  Object.entries(answers.value).forEach(([id, answer]) => {
    console.log(`🔍 [DEBUG ANSWERS] ID: ${id} (${typeof id}) -> Status: ${answer.status}, Keterangan: "${answer.keterangan}"`);
  });
  
  console.log("🔍 [DEBUG ANSWERS] Questions:", questions.value.map(q => ({ id: q.id, name: q.item_name })));
  
  alert(`Debug info logged to console. Answers count: ${Object.keys(answers.value).length}, Questions count: ${questions.value.length}`);
};

const fetchChecklist = async (vehicleType) => {
  try {
    console.log("📡 [FETCH] Calling /p2h/checklist-items...");
    console.log("📡 [FETCH] Vehicle Type to filter:", vehicleType);
    const response = await api.get("/p2h/checklist-items");
    const allQuestions = response.data.payload;
    console.log("📋 [FETCH] Total questions dari API:", allQuestions.length);
    console.log("📋 [FETCH] Sample question:", allQuestions[0]);

    // Debug: tampilkan semua vehicle_tags yang ada
    const allVehicleTags = allQuestions.map(q => q.vehicle_tags);
    console.log("📋 [FETCH] All vehicle_tags in questions:", allVehicleTags);
    
    // Cari yang mengandung vehicleType (case insensitive)
    const exactMatches = allQuestions.filter(
      (q) => q.vehicle_tags && q.vehicle_tags.includes(vehicleType),
    );
    console.log("📋 [FETCH] Exact matches for", vehicleType, ":", exactMatches.length);
    
    // Jika tidak ada exact match, coba case insensitive
    const caseInsensitiveMatches = allQuestions.filter(
      (q) => q.vehicle_tags && q.vehicle_tags.some(tag => 
        tag.toLowerCase().includes(vehicleType.toLowerCase()) ||
        vehicleType.toLowerCase().includes(tag.toLowerCase())
      )
    );
    console.log("📋 [FETCH] Case insensitive matches for", vehicleType, ":", caseInsensitiveMatches.length);
    
    questions.value = exactMatches.length > 0 ? exactMatches : caseInsensitiveMatches;
    console.log(
      "✅ [FILTER] Final questions untuk",
      vehicleType,
      ":",
      questions.value.length,
    );

    if (questions.value.length === 0) {
      console.log("❌ [FILTER] No questions found! Vehicle tags available:");
      allQuestions.forEach((q, idx) => {
        if (idx < 10) { // Log first 10 untuk avoid spam
          console.log(`   Question ${idx + 1}: ${q.item_name} -> Tags: ${q.vehicle_tags}`);
        }
      });
    }

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
      console.log(`📝 [INIT] Answer for question ${q.id} (${typeof q.id}): ${q.item_name}`);
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
    console.log(`🔍 [VALIDATION] Checking question ${qId}: status="${ans.status}", keterangan="${ans.keterangan}"`);
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

    // Konversi selectedShift ke shift_number untuk backend
    let shiftNum = null;
    if (selectedShift.value) {
      const shiftStr = selectedShift.value.toString();
      console.log("🔄 [SHIFT] Converting shift:", shiftStr, typeof shiftStr);
      
      if (shiftStr === "non-shift" || shiftStr === "0") {
        shiftNum = 0; // Non-shift
      } else if (shiftStr === "long-shift-1" || shiftStr === "11") {
        shiftNum = 11; // Long shift 1
      } else if (shiftStr === "long-shift-2" || shiftStr === "12") {
        shiftNum = 12; // Long shift 2
      } else {
        shiftNum = parseInt(shiftStr); // Regular shift 1/2/3
      }
      console.log("🔄 [SHIFT] Converted to:", shiftNum, typeof shiftNum);
    }

    const payload = {
      vehicle_id: vehicleData.value.id,
      shift_number: shiftNum,
      details: Object.keys(answers.value).map((id) => ({
        checklist_item_id: parseInt(id), // Pastikan integer
        status: answers.value[id].status.toLowerCase(), // Convert ke lowercase untuk backend
        keterangan: answers.value[id].keterangan || "", // Pastikan string tidak null
      })),
    };

    // Validasi payload sebelum kirim
    console.log("🔍 [VALIDATION] Validating payload...");
    console.log("🔍 [VALIDATION] vehicle_id:", payload.vehicle_id, typeof payload.vehicle_id);
    console.log("🔍 [VALIDATION] shift_number:", payload.shift_number, typeof payload.shift_number);
    console.log("🔍 [VALIDATION] details count:", payload.details.length);
    
    // Validasi vehicle_id
    if (!payload.vehicle_id || typeof payload.vehicle_id !== 'number') {
      alert("❌ Error: vehicle_id tidak valid");
      return;
    }
    
    // Validasi shift_number  
    if (payload.shift_number === null || typeof payload.shift_number !== 'number') {
      alert("❌ Error: shift_number tidak valid");
      return;
    }
    
    // Validasi details
    if (!payload.details || payload.details.length === 0) {
      alert("❌ Error: Tidak ada detail checklist");
      return;
    }
    
    // Validasi setiap detail
    for (let i = 0; i < payload.details.length; i++) {
      const detail = payload.details[i];
      console.log(`🔍 [VALIDATION] Detail ${i + 1}:`, detail);
      
      if (!detail.checklist_item_id) {
        alert(`❌ Error: checklist_item_id kosong pada item ${i + 1}`);
        return;
      }
      
      if (!detail.status || !['normal', 'abnormal', 'warning'].includes(detail.status)) {
        alert(`❌ Error: Status tidak valid pada item ${i + 1}: ${detail.status}`);
        return;
      }
      
      // Keterangan wajib jika status bukan normal
      if ((detail.status === 'abnormal' || detail.status === 'warning') && !detail.keterangan?.trim()) {
        alert(`❌ Error: Keterangan wajib diisi untuk status ${detail.status}`);
        return;
      }
    }
    
    console.log("✅ [VALIDATION] Payload valid, proceeding with submit...");

    console.log("📤 Payload yang dikirim:", JSON.stringify(payload, null, 2));
    
    try {
      const response = await api.post("/p2h/submit", payload);
      console.log("✅ Submit berhasil:", response.data);
    } catch (error) {
      console.error("❌ Submit error:", error);
      console.error("❌ Error response:", error.response);
      console.error("❌ Error data:", error.response?.data);
      console.error("❌ Error status:", error.response?.status);
      console.error("❌ Error headers:", error.response?.headers);
      console.error("❌ Full error object:", JSON.stringify(error.response?.data, null, 2));
      
      // Extract detailed error message
      let errorMessage = "Gagal mengirim laporan";
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map(err => 
            `${err.loc?.join('.')} - ${err.msg}`
          ).join(', ');
        } else {
          errorMessage = JSON.stringify(error.response.data.detail);
        }
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      alert(`Error: ${errorMessage}`);
      return; // Exit early on error
    }

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
            <template v-if="isLoadingUserName"> Selamat datang... </template>
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
              Toleransi pengisian: 1 Jam sebelum shift (mulai
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
                  Non Shift (07:00 - 16:00)
                </option>
                <option value="long-shift-1" class="text-zinc-900">
                  Long Shift 1 (07:00 - 19:00)
                </option>
                <option value="long-shift-2" class="text-zinc-900">
                  Long Shift 2 (19:00 - 07:00)
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
          class="p-6 bg-white rounded-2xl shadow-sm border border-zinc-200 space-y-4"
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
                placeholder="Cari nomor lambung atau nomor polisi"
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
                v-if="vehicleData.no_lambung"
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
                v-if="vehicleData.warna_no_lambung"
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

                <!-- Debug Info Section -->
                <div class="mt-3 pt-2 border-t border-gray-300">
                  <details class="cursor-pointer">
                    <summary class="text-xs font-bold text-gray-600 hover:text-gray-800">
                      🔧 Debug Info (Klik untuk expand)
                    </summary>
                    <div class="mt-2 text-xs text-gray-600 space-y-1 bg-gray-50 p-2 rounded">
                      <p><strong>Can Submit:</strong> {{ p2hStatus?.canSubmit }}</p>
                      <p><strong>Current Shift:</strong> {{ p2hStatus?.currentShift }}</p>
                      <p><strong>Shifts Completed:</strong> {{ p2hStatus?.shiftsCompleted }}</p>
                      <p><strong>Color Code:</strong> {{ p2hStatus?.color }}</p>
                      <p><strong>P2H Completed Today:</strong> {{ p2hStatus?.completed }}</p>
                      <p><strong>Questions Available:</strong> {{ questions.length }}</p>
                      <p><strong>Is Authenticated:</strong> {{ isAuthenticated }}</p>
                      <p><strong>Current Shift Done:</strong> {{ 
                        p2hStatus?.shiftsCompleted?.includes(p2hStatus?.currentShift) 
                      }}</p>
                      <p><strong>Is Travel/Light Vehicle:</strong> {{ 
                        vehicleData?.vehicle_type?.toLowerCase().includes('travel') ||
                        vehicleData?.vehicle_type?.toLowerCase().includes('light vehicle')
                      }}</p>
                      
                      <!-- Force Fetch Button untuk debugging -->
                      <div class="mt-2 pt-2 border-t border-gray-400 space-y-1">
                        <button 
                          @click="forceFetchChecklist" 
                          class="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white text-xs rounded font-bold mr-2"
                        >
                          🔧 Force Fetch Checklist
                        </button>
                        <button 
                          @click="debugAnswers" 
                          class="px-3 py-1 bg-green-500 hover:bg-green-600 text-white text-xs rounded font-bold"
                        >
                          🔍 Debug Answers
                        </button>
                      </div>
                    </div>
                  </details>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Message ketika tidak bisa mengisi P2H -->
        <div 
          v-if="vehicleData && (!p2hStatus?.canSubmit || (p2hStatus?.shiftsCompleted && p2hStatus.shiftsCompleted.includes(p2hStatus?.currentShift))) && !(vehicleData.vehicle_type?.toLowerCase().includes('travel') || vehicleData.vehicle_type?.toLowerCase().includes('light vehicle'))"
          class="p-6 bg-blue-50 border-2 border-blue-300 rounded-2xl"
        >
          <div class="flex items-center gap-2 text-blue-900 mb-3">
            <InformationCircleIcon class="h-5 w-5" />
            <h3 class="font-bold text-lg">Informasi P2H</h3>
          </div>
          
          <div v-if="p2hStatus?.completed" class="space-y-2">
            <p class="text-sm font-semibold text-blue-800">
              ✅ P2H untuk kendaraan ini sudah selesai untuk hari ini.
            </p>
            <p class="text-xs text-blue-700">
              Shift yang sudah diisi: {{ p2hStatus.shiftsCompleted?.join(', ') || 'Tidak ada' }}
            </p>
          </div>
          
          <div v-else-if="!p2hStatus?.canSubmit" class="space-y-2">
            <p class="text-sm font-semibold text-blue-800">
              ❌ Tidak dapat mengisi P2H saat ini.
            </p>
            <p class="text-xs text-blue-700">
              Alasan: {{ p2hStatus?.message || 'Belum waktunya atau sudah terisi untuk shift saat ini' }}
            </p>
          </div>
          
          <div v-else class="space-y-2">
            <p class="text-sm font-semibold text-blue-800">
              ⏰ P2H untuk shift saat ini sudah diisi.
            </p>
            <p class="text-xs text-blue-700">
              Shift {{ p2hStatus?.currentShift }} sudah selesai di-P2H.
            </p>
          </div>
        </div>

        <!-- Message khusus untuk Travel -->
        <div 
          v-if="vehicleData && (vehicleData.vehicle_type?.toLowerCase().includes('travel') || vehicleData.vehicle_type?.toLowerCase().includes('light vehicle')) && questions.length === 0 && isAuthenticated"
          class="p-6 bg-orange-50 border-2 border-orange-300 rounded-2xl"
        >
          <div class="flex items-center gap-2 text-orange-900 mb-3">
            <ExclamationTriangleIcon class="h-5 w-5" />
            <h3 class="font-bold text-lg">Travel/Light Vehicle - Checklist Tidak Ditemukan</h3>
          </div>
          <div class="space-y-2">
            <p class="text-sm font-semibold text-orange-800">
              🚗 Kendaraan Travel/Light Vehicle terdeteksi, namun checklist tidak dapat dimuat.
            </p>
            <p class="text-xs text-orange-700 space-y-1">
              <span class="block">• Kemungkinan belum ada checklist untuk tipe "{{ vehicleData.vehicle_type }}"</span>
              <span class="block">• Atau ada masalah dengan konfigurasi backend</span>
              <span class="block">• Gunakan tombol "Force Fetch" di debug info untuk mencoba lagi</span>
            </p>
          </div>
        </div>

        <!-- Message ketika tidak login -->
        <div 
          v-if="vehicleData && !isAuthenticated && p2hStatus?.color !== 'green'"
          class="p-6 bg-yellow-50 border-2 border-yellow-400 rounded-2xl"
        >
          <div class="flex items-center gap-2 text-yellow-900 mb-3">
            <ExclamationTriangleIcon class="h-5 w-5" />
            <h3 class="font-bold text-lg">Login Diperlukan</h3>
          </div>
          <p class="text-sm font-semibold text-yellow-800 mb-3">
            Kendaraan ini belum di-P2H. Silakan login untuk mengisi form P2H.
          </p>
          <button
            @click="handleLoginRedirect"
            class="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white font-bold text-sm rounded-lg transition-colors"
          >
            Login Sekarang
          </button>
        </div>

        <section
          v-if="
            vehicleData && 
            isAuthenticated && 
            questions.length > 0 && 
            (p2hStatus?.color !== 'green' || 
             (vehicleData.vehicle_type?.toLowerCase().includes('travel') || 
              vehicleData.vehicle_type?.toLowerCase().includes('light vehicle')))
          "
          class="space-y-6 pb-5"
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
              <p class="font-bold text-zinc-800 text-base mt-5 mb-3">
                {{ q.pertanyaan }}
              </p>

              <div class="grid grid-cols-1 gap-0">
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
