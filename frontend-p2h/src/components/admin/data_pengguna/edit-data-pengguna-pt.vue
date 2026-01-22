<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import Aside from "../../bar/aside.vue";
import HeaderAdmin from "../../bar/header_admin.vue";
import {
  XMarkIcon,
  PencilSquareIcon,
  ChevronLeftIcon,
} from "@heroicons/vue/24/solid";
import { useSidebarProvider } from "../../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();

const router = useRouter();
const route = useRoute();
const showEditAkun = ref(false);
const isStatusAktif = ref(true);

// Dummy data
const adminName = ref("Naufal Andrian");
const adminEmail = ref("naufal@indominco.com");
const adminNoTelepon = ref("081234567890");
const adminTanggalLahir = ref("1990-05-15");
const adminPerusahaan = ref("PT Indominco Mandiri");
const adminDepartemen = ref("IT Department");
const adminStatusKaryawan = ref("Permanent");
const adminPosisiKerja = ref("System Administrator");
const roleKerja = ref("Admin");

const openEditAkun = () => {
  showEditAkun.value = true;
};

const closeEditAkun = () => {
  showEditAkun.value = false;
};

const goBack = () => {
  router.push("/data-pengguna-pt");
};

// Load user data dari localStorage berdasarkan ID
onMounted(() => {
  const userData = localStorage.getItem('currentUserData');
  if (userData) {
    const user = JSON.parse(userData);
    adminName.value = user.namaLengkap || '';
    adminEmail.value = user.email || '';
    adminNoTelepon.value = user.noHandphone || '';
    adminPerusahaan.value = user.namaPerusahaan || '';
    adminDepartemen.value = user.departemen || '';
    adminStatusKaryawan.value = user.status || '';
    adminPosisiKerja.value = user.posisi || '';
    roleKerja.value = user.role || '';
    localStorage.removeItem('currentUserData');
  }
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
            class="bg-white rounded-lg shadow-md p-1 pl-5 mb-2 -mt-1 shrink-0"
          >
            <h1 class="text-base font-bold text-[#523E95] text-left">PT Indominco Mandiri</h1>
          </div>
          <div
            class="bg-white rounded-lg shadow-md gap-4 p-5 flex-1 flex flex-col overflow-hidden"
          >
            <div class="flex justify-between items-center">
              <div class="flex items-center gap-2">
                <button
                  @click="goBack"
                  class="hover:bg-gray-100 p-1 rounded transition"
                >
                  <ChevronLeftIcon
                    class="w-6 h-6 text-gray-600 hover:text-gray-900 cursor-pointer"
                  />
                </button>
                <h1 class="text-lg font-bold text-black">
                  Detail Data Pengguna PT Indominco Mandiri
                </h1>
              </div>
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
                  v-model="adminName"
                  type="text"
                  placeholder="Nama Lengkap"
                  disabled
                  class="w-full p-2 text-sm border border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">Email</p>
                <input
                  v-model="adminEmail"
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
                  v-model="adminNoTelepon"
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
                  v-model="adminTanggalLahir"
                  type="text"
                  placeholder="hh/bb/tttt"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
            </div>

            <!-- Perusahaan & Departemen-->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">
                  Perusahaan
                </p>
                <input
                  v-model="adminPerusahaan"
                  type="text"
                  placeholder="Perusahaan"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">
                  Departemen
                </p>
                <input
                  v-model="adminDepartemen"
                  type="text"
                  placeholder="Departemen"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
            </div>

            <!-- Status Karyawan & Posisi -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">
                  Status
                </p>
                <input
                  v-model="adminStatusKaryawan"
                  type="text"
                  placeholder="Status karyawan"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">
                  Posisi kerja
                </p>
                <input
                  v-model="adminPosisiKerja"
                  type="text"
                  placeholder="Posisi kerja"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
            </div>

            <!-- Role -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <p class="text-base font-regular text-gray-800 mb-1">Role</p>
                <input
                  v-model="roleKerja"
                  type="text"
                  placeholder="Role"
                  disabled
                  class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md cursor-not-allowed"
                />
              </div>
            </div>

            <!-- Status Karyawan Aktif -->
            <div
              class="flex justify-between items-center bg-[#EEEEEE] p-3 rounded-md border border-[#C3C3C3] mt-2"
            >
              <p class="text-base font-regular text-gray-600">
                Status karyawan aktif
              </p>
              <label class="relative inline-flex items-center cursor-pointer">
                <input
                  v-model="isStatusAktif"
                  type="checkbox"
                  disabled
                  class="sr-only peer"
                />
                <div
                  class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[#A90CF8] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-gray-200 after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#c381e4]"
                ></div>
              </label>
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

              <!-- Status Karyawan Aktif -->
              <div
                class="flex justify-between items-center bg-gray-50 p-4 rounded-md border border-[#C3C3C3] mt-4"
              >
                <p class="text-base font-regular text-gray-800">
                  Status karyawan aktif
                </p>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input
                    v-model="isStatusAktif"
                    type="checkbox"
                    class="sr-only peer"
                  />
                  <div
                    class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[#A90CF8] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#A90CF8]"
                  ></div>
                </label>
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