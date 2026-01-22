<script setup>
import { ref } from "vue";
import NavBar from "../bar/header-user.vue";
import Footer from "../bar/footer.vue";
import {
  XMarkIcon,
  PencilSquareIcon,
  ChevronRightIcon,
} from "@heroicons/vue/24/solid";

const showEditAkun = ref(false);

const openEditAkun = () => {
  showEditAkun.value = true;
};

const closeEditAkun = () => {
  showEditAkun.value = false;
};
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <!-- Navbar -->
    <NavBar />

    <!-- Kontent Profil -->
    <main
      class="flex-1 flex items-start md:items-center justify-center bg-cover bg-center bg-no-repeat px-4 pt-24 md:pt-8 pb-40 md:pb-20 overflow-y-auto"
      style="background-image: url(/image_asset/Backgrond.png)"
    >
      <div
        class="w-full h-auto flex flex-col gap-4 bg-white rounded-xl shadow-lg max-w-2xl md:max-w-4xl p-4 md:p-7 mt-2 md:mt-0">
        <div class="flex justify-end">
          <button
            @click="openEditAkun"
            class="px-7 py-1 text-xs md:text-sm font-semilight bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-md hover:opacity-90 transition">
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
              placeholder="Nama Lengkap"
              class="w-full p-2 text-sm border border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md"
            />
          </div>
          <div>
            <p class="text-base font-regular text-gray-800 mb-1">Email</p>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="email@example.com"
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
              placeholder="081xxxxxxxx"
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
              placeholder="hh/bb/tttt"
              class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md"
            />
          </div>
          <div>
            <p class="text-base font-regular text-gray-800 mb-1">Perusahaan</p>
            <input
              id="company"
              name="company"
              type="text"
              placeholder="Perusahaan"
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
            placeholder="Departemen"
            class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md mb-1"
          />
        </div>
        <div>
          <p class="text-base font-regular text-gray-800 mb-1">Status karyawan</p>
          <input
            id="work_status"
            name="work_status"
            type="text"
            placeholder="Status karyawan"
            class="w-full p-2 border text-sm border-[#C3C3C3] bg-[#EEEEEE] text-[#777777] rounded-md mb-1"
          />
        </div>

        <div>
          <p class="text-base font-regular text-gray-800 mb-1">Posisi kerja</p>
          <input
            id="position"
            name="position"
            type="text"
            placeholder="Posisi kerja"
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
            <label for="edit_nama" class="block text-base font-medium text-black mb-2 mt-4"
              >Nama Lengkap</label
            >
            <div class="relative">
              <input
                id="edit_nama"
                name="edit_nama"
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
            <label for="edit_phone" class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Nomor Handphone</label
            >
            <div class="relative">
              <input
                id="edit_phone"
                name="edit_phone"
                type="tel"
                placeholder="081xxxxxxxx"
                class="w-full p-2 pr-10 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
              />
              <PencilSquareIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
              />
            </div>
          </div>
          <div>
            <label for="edit_company" class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Perusahaan</label
            >
            <div class="relative">
              <input
                id="edit_company"
                name="edit_company"
                type="text"
                placeholder="Nama perusahaan"
                class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
              />
              <ChevronRightIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
              />
            </div>
          </div>
          <div>
            <label for="edit_department" class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Departemen</label
            >
            <div class="relative">
              <input
                id="edit_department"
                name="edit_department"
                type="text"
                placeholder="Nama departemen"
                class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
              />
              <ChevronRightIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
              />
            </div>
          </div>
          <div>
            <label for="edit_position" class="block text-base font-medium text-gray-800 mb-2 mt-2"
              >Posisi kerja</label
            >
            <div class="relative">
              <input
                id="edit_position"
                name="edit_position"
                type="text"
                placeholder="Posisi kerja"
                class="w-full p-2 pr-10 border text-sm border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
              />
              <ChevronRightIcon
                class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
              />
            </div>
          </div>

          <div class="flex justify-center mt-6">
            <button
              class="px-8 md:px-10 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular"
            >
              Simpan
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>
