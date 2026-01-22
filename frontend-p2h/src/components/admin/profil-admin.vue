<script setup>
import { ref, onMounted, computed } from "vue";
import Aside from "../bar/aside.vue";
import HeaderAdmin from "../bar/header_admin.vue";
import {
  XMarkIcon,
  PencilSquareIcon,
} from "@heroicons/vue/24/solid";
import { useUserProfile } from "../../composables/useUserProfile";
import { useSidebarProvider } from "../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();

const showEditAkun = ref(false);

// Use composable for user profile
const { userProfile, fetchUserProfile, isLoading } = useUserProfile();

// Computed properties untuk data yang akan ditampilkan
const adminName = computed(() => userProfile.value?.full_name || 'Loading...');
const adminEmail = computed(() => userProfile.value?.email || 'Loading...');
const adminNoTelepon = computed(() => userProfile.value?.phone_number || 'Loading...');
const adminTanggalLahir = computed(() => {
  if (!userProfile.value?.birth_date) return 'Loading...';
  // Format tanggal dari YYYY-MM-DD ke DD/MM/YYYY
  const date = new Date(userProfile.value.birth_date);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
});
const adminPerusahaan = computed(() => userProfile.value?.company?.nama_perusahaan || 'Loading...');
const adminDepartemen = computed(() => userProfile.value?.department?.nama_department || 'Loading...');
const adminStatusKaryawan = computed(() => userProfile.value?.work_status?.nama_status || 'Loading...');
const adminPosisiKerja = computed(() => userProfile.value?.position?.nama_posisi || 'Loading...');
const roleKerja = computed(() => {
  const roleMap = {
    'superadmin': 'Super Administrator',
    'admin': 'Administrator',
    'user': 'User'
  };
  return roleMap[userProfile.value?.role] || 'Loading...';
});

const openEditAkun = () => {
  showEditAkun.value = true;
};

const closeEditAkun = () => {
  showEditAkun.value = false;
};

// Fetch profile saat component mounted
onMounted(async () => {
  await fetchUserProfile();
});
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <div class="flex flex-1 overflow-hidden">
      <Aside />

      <div class="flex flex-col flex-1 overflow-hidden">
        <HeaderAdmin />

        <!-- Content -->
        <main class="bg-[#EFEFEF] flex-1 flex flex-col p-3 overflow-hidden">
          <div
            class="bg-white rounded-lg shadow-md gap-4 p-5 flex-1 flex flex-col overflow-hidden"
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
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">Nama</p>
                <input
                  :value="adminName"
                  type="text"
                  placeholder="Nama Lengkap"
                  disabled
                  class="w-full p-2 text-sm border border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">Email</p>
                <input
                  :value="adminEmail"
                  type="text"
                  placeholder="email@example.com"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
            </div>

            <!-- Nomor Telepon dan Tanggal Lahir -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">
                  Nomor Telepon
                </p>
                <input
                  :value="adminNoTelepon"
                  type="text"
                  placeholder="081xxxxxxxx"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">
                  Tanggal Lahir
                </p>
                <input
                  :value="adminTanggalLahir"
                  type="text"
                  placeholder="hh/bb/tttt"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
            </div>

            <!-- Perusahaan -->
            <div>
              <p class="text-base font-regular text-gray-800 mb-1">
                Perusahaan
              </p>
              <input
                :value="adminPerusahaan"
                type="text"
                placeholder="Perusahaan"
                disabled
                class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
              />
            </div>

            <!-- Departemen -->
            <div>
              <p class="text-base font-regular text-gray-800 mb-1">
                Departemen
              </p>
              <input
                :value="adminDepartemen"
                type="text"
                placeholder="Departemen"
                disabled
                class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
              />
            </div>

            <!-- Status Karyawan -->
            <div>
              <p class="text-base font-regular text-gray-800 mb-1">
                Status karyawan
              </p>
              <input
                :value="adminStatusKaryawan"
                type="text"
                placeholder="Status karyawan"
                disabled
                class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
              />
            </div>

            <!-- Posisi Kerja -->
            <div>
              <p class="text-base font-regular text-gray-800 mb-1">
                Posisi kerja
              </p>
              <input
                :value="adminPosisiKerja"
                type="text"
                placeholder="Posisi kerja"
                disabled
                class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
              />
            </div>

            <!-- Role-->
            <div>
              <p class="text-base font-regular text-gray-800 mb-1">
                Role
              </p>
              <input
                :value="roleKerja"
                type="text"
                placeholder="Role"
                disabled
                class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
              />
            </div>
          </div>

          <!-- Konten Edit akun -->
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
                  <XMarkIcon
                    class="w-6 h-6 text-gray-600 hover:text-gray-900"
                  />
                </button>
              </div>

              <div>
                <label class="block text-base font-medium text-black mb-2 mt-4"
                  >Nama Lengkap</label
                >
                <div class="relative">
                  <input
                    type="text"
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
                  class="block text-base font-medium text-gray-800 mb-2 mt-2"
                  >Nomor Handphone</label
                >
                <div class="relative">
                  <input
                    type="text"
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
                  class="block text-base font-medium text-gray-800 mb-2 mt-2"
                  >Email</label
                >
                <div class="relative">
                  <input
                    type="text"
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
                  class="block text-base font-medium text-gray-800 mb-2 mt-2"
                  >Tanggal Lahir</label
                >
                <input
                  type="date"
                  class="w-full p-2 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
                />
              </div>
              

              <div class="flex justify-end gap-3 mt-6">
                <button
                  class="px-8 md:px-10 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular"
                >
                  Simpan
                </button>
                <button
                  @click="closeEditAkun"
                  class="px-6 md:px-6 py-2 text-sm md:text-base border border-gray-300 bg-red-600 text-white rounded-xl hover:bg-red-700 transition font-regular"
                >
                  Batal
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>