<script setup>
import { ref, onMounted, computed } from "vue";
import NavBar from "../bar/header-user.vue";
import Footer from "../bar/footer.vue";
import {
  XMarkIcon,
  PencilSquareIcon,
  ChevronRightIcon,
  ChevronDownIcon,
} from "@heroicons/vue/24/solid";
import { api } from "../../services/api";

const showEditAkun = ref(false);
const isLoading = ref(false);
const isSaving = ref(false);

// User data for display
const userData = ref({
  id: null,
  full_name: "",
  email: "",
  phone_number: "",
  birth_date: "",
  company_id: null,
  department_id: null,
  work_status_id: null,
  position_id: null,
  // Display names
  company_name: "",
  department_name: "",
  work_status_name: "",
  position_name: "",
});

// Edit form data (separate from display)
const editForm = ref({
  full_name: "",
  phone_number: "",
  email: "",
  company_id: null,
  department_id: null,
  work_status_id: null,
  position_id: null,
});

// Master data for dropdowns
const companies = ref([]);
const departments = ref([]);
const positions = ref([]);
const workStatuses = ref([]);

// Fetch master data for dropdowns
const fetchMasterData = async () => {
  try {
    const [companiesRes, departmentsRes, positionsRes, workStatusesRes] =
      await Promise.all([
        api.get("/master-data/companies"),
        api.get("/master-data/departments"),
        api.get("/master-data/positions"),
        api.get("/master-data/work-statuses"),
      ]);

    companies.value = companiesRes.data.payload || [];
    departments.value = departmentsRes.data.payload || [];
    positions.value = positionsRes.data.payload || [];
    workStatuses.value = workStatusesRes.data.payload || [];
  } catch (error) {
    console.error("❌ Gagal fetch master data:", error);
  }
};

// Fetch user profile data
const fetchUserProfile = async () => {
  try {
    isLoading.value = true;
    console.log("🔄 Fetching user profile...");
    const response = await api.get("/users/me");
    console.log("✅ User profile fetched:", response.data);

    const user = response.data.payload;
    userData.value = {
      id: user.id,
      full_name: user.full_name || "",
      email: user.email || "",
      phone_number: user.phone_number || "",
      birth_date: user.birth_date || "",
      company_id: user.company_id,
      department_id: user.department_id,
      work_status_id: user.work_status_id,
      position_id: user.position_id,
      // Access nested object names
      company_name: user.company?.nama_perusahaan || "-",
      department_name: user.department?.nama_department || "-",
      work_status_name: user.work_status?.nama_status || "-",
      position_name: user.position?.nama_posisi || "-",
    };
  } catch (error) {
    console.error("❌ Gagal fetch user profile:", error);
    if (error.response?.status === 401) {
      alert("Sesi Anda telah berakhir. Silakan login kembali.");
    } else {
      alert(
        "Gagal memuat profil: " +
          (error.response?.data?.detail || error.message),
      );
    }
  } finally {
    isLoading.value = false;
  }
};

const openEditAkun = () => {
  // Copy current data to edit form
  editForm.value = {
    full_name: userData.value.full_name,
    phone_number: userData.value.phone_number,
    email: userData.value.email,
    company_id: userData.value.company_id,
    department_id: userData.value.department_id,
    work_status_id: userData.value.work_status_id,
    position_id: userData.value.position_id,
  };
  showEditAkun.value = true;
};

const closeEditAkun = () => {
  showEditAkun.value = false;
};

const handleSaveProfile = async () => {
  try {
    isSaving.value = true;

    // Prepare update payload
    const payload = {
      full_name: editForm.value.full_name,
      phone_number: editForm.value.phone_number,
      email: editForm.value.email || null,
      company_id: editForm.value.company_id || null,
      department_id: editForm.value.department_id || null,
      work_status_id: editForm.value.work_status_id || null,
      position_id: editForm.value.position_id || null,
    };

    console.log("📤 Updating profile:", payload);
    const response = await api.put("/users/me", payload);
    console.log("✅ Profile updated:", response.data);

    alert("Profil berhasil diperbarui!");
    closeEditAkun();

    // Refresh profile data
    await fetchUserProfile();
  } catch (error) {
    console.error("❌ Gagal update profil:", error);
    alert(
      "Gagal menyimpan perubahan: " +
        (error.response?.data?.detail || error.message),
    );
  } finally {
    isSaving.value = false;
  }
};

onMounted(async () => {
  await fetchMasterData();
  await fetchUserProfile();
});
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <!-- Navbar -->
    <NavBar />

    <!-- Kontent Profil -->
    <main
      class="flex-1 flex items-start md:items-center justify-center bg-cover bg-center bg-no-repeat px-4 pt-24 md:pt-8 pb-40 md:pb-20 overflow-y-auto"
      style="background-image: url(/image_asset/BG_2.png)"
    >
      <div
        class="w-full h-auto flex flex-col gap-4 bg-white rounded-xl shadow-lg max-w-2xl md:max-w-4xl p-4 md:p-7 mt-2 md:mt-0"
      >
        <div class="flex justify-end">
          <button
            @click="openEditAkun"
            class="px-7 py-1 text-xs md:text-sm font-semilight bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-md hover:opacity-90 transition"
          >
            Edit akun
          </button>
        </div>

        <!-- Nama dan Email -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <p class="text-base font-regular text-gray-800 mb-1">Nama</p>
            <input
              id="nama"
              name="nama"
              type="text"
              v-model="userData.full_name"
              placeholder="Nama Lengkap"
              readonly
              class="w-full p-2 text-sm border border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md"
            />
          </div>
          <div>
            <p class="text-base font-regular text-gray-800 mb-1">Email</p>
            <input
              id="email"
              name="email"
              type="email"
              v-model="userData.email"
              placeholder="email@example.com"
              readonly
              class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md"
            />
          </div>
        </div>

        <!-- Nomor Telepon, Tanggal Lahir, dan Perusahaan -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div>
            <p class="text-base font-regular text-gray-800 mb-1">
              Nomor Telepon
            </p>
            <input
              id="phone_number"
              name="phone_number"
              type="tel"
              v-model="userData.phone_number"
              placeholder="081xxxxxxxx"
              readonly
              class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md"
            />
          </div>
          <div>
            <p class="text-base font-regular text-gray-800 mb-1">
              Tanggal Lahir
            </p>
            <input
              id="birth_date"
              name="birth_date"
              type="date"
              v-model="userData.birth_date"
              placeholder="hh/bb/tttt"
              readonly
              class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md"
            />
          </div>
          <div>
            <p class="text-base font-regular text-gray-800 mb-1">Perusahaan</p>
            <input
              id="company"
              name="company"
              type="text"
              v-model="userData.company_name"
              placeholder="Perusahaan"
              readonly
              class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md"
            />
          </div>
        </div>
        <div>
          <p class="text-base font-regular text-gray-800 mb-1">Departemen</p>
          <input
            id="department"
            name="department"
            type="text"
            v-model="userData.department_name"
            placeholder="Departemen"
            readonly
            class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md mb-1"
          />
        </div>
        <div>
          <p class="text-base font-regular text-gray-800 mb-1">
            Status karyawan
          </p>
          <input
            id="work_status"
            name="work_status"
            type="text"
            v-model="userData.work_status_name"
            placeholder="Status karyawan"
            readonly
            class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md mb-1"
          />
        </div>

        <div>
          <p class="text-base font-regular text-gray-800 mb-1">Posisi kerja</p>
          <input
            id="position"
            name="position"
            type="text"
            v-model="userData.position_name"
            placeholder="Posisi kerja"
            readonly
            class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md mb-1"
          />
        </div>
      </div>

      <!-- Kontent Edit akun -->
      <div
        v-if="showEditAkun"
        class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
      >
        <div
          class="bg-white rounded-lg w-full max-w-md md:max-w-xl max-h-[90vh] overflow-y-auto shadow-[0_4px_6px_rgba(0,0,0,0.1)] p-6 md:p-8"
        >
          <div
            class="flex justify-between items-center mb-4 pb-3 border-b border-gray-200"
          >
            <h2 class="text-lg md:text-xl font-semibold text-gray-900">
              Edit Profil
            </h2>
            <button
              @click="closeEditAkun"
              class="shrink-0 p-1 hover:bg-gray-100 rounded-md transition"
            >
              <XMarkIcon class="w-6 h-6 text-gray-600 hover:text-gray-900" />
            </button>
          </div>

          <div>
            <label
              for="edit_nama"
              class="block text-base font-medium text-black mb-2 mt-4"
              >Nama Lengkap</label
            >
            <div class="relative">
              <input
                id="edit_nama"
                name="edit_nama"
                type="text"
                v-model="editForm.full_name"
                placeholder="Masukkan nama"
                class="w-full p-2 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
              />
              <PencilSquareIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
              />
            </div>
          </div>
          <div>
            <label
              for="edit_phone"
              class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Nomor Handphone</label
            >
            <div class="relative">
              <input
                id="edit_phone"
                name="edit_phone"
                type="tel"
                v-model="editForm.phone_number"
                placeholder="081xxxxxxxx"
                class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
              />
              <PencilSquareIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
              />
            </div>
          </div>
          <div>
            <label
              for="edit_email"
              class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Email</label
            >
            <div class="relative">
              <input
                id="edit_email"
                name="edit_email"
                type="email"
                v-model="editForm.email"
                placeholder="email@example.com"
                class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
              />
              <PencilSquareIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
              />
            </div>
          </div>
          <div>
            <label
              for="edit_company"
              class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Perusahaan</label
            >
            <div class="relative">
              <select
                id="edit_company"
                name="edit_company"
                v-model="editForm.company_id"
                class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8] appearance-none"
              >
                <option :value="null">-- Pilih Perusahaan --</option>
                <option
                  v-for="company in companies"
                  :key="company.id"
                  :value="company.id"
                >
                  {{ company.nama_perusahaan }}
                </option>
              </select>
              <ChevronDownIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3] pointer-events-none"
              />
            </div>
          </div>
          <div>
            <label
              for="edit_department"
              class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Departemen</label
            >
            <div class="relative">
              <select
                id="edit_department"
                name="edit_department"
                v-model="editForm.department_id"
                class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8] appearance-none"
              >
                <option :value="null">-- Pilih Departemen --</option>
                <option
                  v-for="dept in departments"
                  :key="dept.id"
                  :value="dept.id"
                >
                  {{ dept.nama_department }}
                </option>
              </select>
              <ChevronDownIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3] pointer-events-none"
              />
            </div>
          </div>
          <div>
            <label
              for="edit_work_status"
              class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Status Karyawan</label
            >
            <div class="relative">
              <select
                id="edit_work_status"
                name="edit_work_status"
                v-model="editForm.work_status_id"
                class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8] appearance-none"
              >
                <option :value="null">-- Pilih Status --</option>
                <option
                  v-for="status in workStatuses"
                  :key="status.id"
                  :value="status.id"
                >
                  {{ status.nama_status }}
                </option>
              </select>
              <ChevronDownIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3] pointer-events-none"
              />
            </div>
          </div>
          <div>
            <label
              for="edit_position"
              class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Posisi Kerja</label
            >
            <div class="relative">
              <select
                id="edit_position"
                name="edit_position"
                v-model="editForm.position_id"
                class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8] appearance-none"
              >
                <option :value="null">-- Pilih Posisi --</option>
                <option v-for="pos in positions" :key="pos.id" :value="pos.id">
                  {{ pos.nama_posisi }}
                </option>
              </select>
              <ChevronDownIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3] pointer-events-none"
              />
            </div>
          </div>

          <div class="flex justify-center mt-6">
            <button
              @click="handleSaveProfile"
              :disabled="isSaving"
              class="px-8 md:px-10 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular disabled:opacity-50"
            >
              {{ isSaving ? "Menyimpan..." : "Simpan" }}
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>
