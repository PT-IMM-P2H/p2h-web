<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import NavBar from "../bar/header-user.vue";
import Footer from "../bar/footer.vue";
import { InformationCircleIcon } from "@heroicons/vue/24/outline";

const router = useRouter();
const currentDate = ref("");

onMounted(() => {
  // Format tanggal hari ini
  const today = new Date();
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  currentDate.value = today.toLocaleDateString("id-ID", options);
});

const handleWaLink = () => {
  window.open("https://wa.me/6282254442400", "_blank");
};

const handleKembali = () => {
  router.push("/login");
};
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <!-- Navbar -->
    <NavBar />

    <!-- Content -->
    <main
      class="flex-1 flex items-center justify-center bg-cover bg-center bg-no-repeat py-20 mb-10 overflow-y-auto"
      style="background-image: url(/image_asset/BG_2.png); background-attachment: fixed;"
    >
      <div class="p-4 m-3 bg-white rounded-lg shadow-lg w-full max-w-6xl">
        <div class="flex justify-between items-center mb-4">
          <img
            src="/image_asset/2_Ptimm.png"
            alt="Logo"
            class="h-7 md:h-8 w-auto shrink-0"
          />
          <p class="text-base text-black font-bold">{{ currentDate }}</p>
        </div>
        <hr class="mt-1 mb-3 border-gray-300" />

        <h1 class="text-2xl font-bold mb-1 text-gray-800 text-start">
          Hasil Pelaksanaan Pemeriksaan Harian Kendaraan
        </h1>
        <p class="text-sm text-gray-600 text-left">
          <InformationCircleIcon class="w-4 h-4 inline-block text-gray-500" />
          You hava submitted the form at {{ new }}
        </p>

        <!-- Hasil Normal -->
        <div
          class="flex items-start gap-3 mb-2 mt-2 p-2 bg-green-100 border-l-4 border-green-500 rounded"
        >
          <p class="text-black font-medium text-lg leading-relaxed">
            Kondisi kendaraan : <span class="font-bold">Normal</span>
          </p>
        </div>

        <!-- Pengumuman Box Normal -->
        <div
          class="flex items-start gap-3 mb-4 mt-4 p-4 bg-red-50 border-l-4 border-red-500 rounded"
        >
          <div class="text-black font-semibold text-sm leading-relaxed italic">
            <ul class="list-disc list-inside -space-y-1">
              <li>Gunakan APD lengkap dan sabuk pengaman</li>
              <li>
                Batas kecepatan:
                <ul class="list-circle list-inside ml-4 -space-y-1">
                  <li>Light Vehicle (LV): maksimal 60 km/jam</li>
                  <li>Bus: maksimal 50 km/jam</li>
                </ul>
              </li>
              <li>
                Kurangi kecepatan di tikungan, persimpangan, dan area alat berat
              </li>
              <li>Gunakan radio komunikasi selama berkendara</li>
              <li>Dilarang menggunakan HP saat berkendara</li>
              <li>Selalu patuhi rambu lalu lintas</li>
              <li>
                Nyalakan lampu besar saat berada di area tambang dan matikan
                saat berada di luar area tambang
              </li>
              <li>Jangan mengemudi dalam kondisi lelah atau mengantuk</li>
              <li>Pastikan kendaraan dalam kondisi bersih dan rapi</li>
            </ul>
          </div>
        </div>

        <!-- Hasil Abnormal -->
        <div
          class="flex items-start gap-3 mb-2 mt-2 p-2 bg-yellow-100 border-l-4 border-yellow-500 rounded"
        >
          <p class="text-black font-medium text-lg leading-relaxed">
            Kondisi kendaraan : <span class="font-bold">Abnormal</span>
          </p>
        </div>
        
        <div
          class="flex items-start gap-3 mb-4 mt-4 p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded"
        >
          <p class="text-black font-semibold text-sm leading-relaxed italic">
            Bagian kendaraan terdapat kerusakan ringan, namun masih dapat digunakan dan perlu dilakukan pemeriksaan atau perbaikan di bengkel.
          </p>
        </div>

        <!-- Pengumuman Box Normal -->
        <div
          class="flex items-start gap-3 mb-4 mt-4 p-4 bg-red-50 border-l-4 border-red-500 rounded"
        >
          <div class="text-black font-semibold text-sm leading-relaxed italic">
            <ul class="list-disc list-inside -space-y-1">
              <li>Gunakan APD lengkap dan sabuk pengaman</li>
              <li>
                Batas kecepatan:
                <ul class="list-circle list-inside ml-4 -space-y-1">
                  <li>Light Vehicle (LV): maksimal 60 km/jam</li>
                  <li>Bus: maksimal 50 km/jam</li>
                </ul>
              </li>
              <li>
                Kurangi kecepatan di tikungan, persimpangan, dan area alat berat
              </li>
              <li>Gunakan radio komunikasi selama berkendara</li>
              <li>Dilarang menggunakan HP saat berkendara</li>
              <li>Selalu patuhi rambu lalu lintas</li>
              <li>
                Nyalakan lampu besar saat berada di area tambang dan matikan
                saat berada di luar area tambang
              </li>
              <li>Jangan mengemudi dalam kondisi lelah atau mengantuk</li>
              <li>Pastikan kendaraan dalam kondisi bersih dan rapi</li>
            </ul>
          </div>
        </div>

        <!-- Hasil Warning -->
        <div
          class="flex items-start gap-3 mb-2 mt-2 p-2 bg-red-100 border-l-4 border-red-500 rounded"
        >
          <p class="text-black font-medium text-lg leading-relaxed">
            Kondisi kendaraan : <span class="font-bold">Warning</span>
          </p>
        </div>
        
        <!-- Pengumuman Box Normal -->
        <div
          class="flex items-start gap-3 mb-4 mt-4 p-4 bg-red-50 border-l-4 border-red-500 rounded"
        >
          <div class="text-black font-semibold text-sm leading-relaxed italic">

            <p class="mb-3 font-bold text-base">
              Bagian kendaraan mengalami kerusakan serius sehingga tidak dapat digunakan dan harus segera dibawa ke bengkel untuk penanganan lebih lanjut.
            </p>
                        <p class="text-red-600 font-bold text-base mb-3 italic underline">
              <InformationCircleIcon class="w-5 h-5 inline-block text-red-600 mr-2" />
              Kendaraan dinyatakan tidak dapat dioperasikan
            </p>
            <p class="font-bold text-base">
              Hubungi Rizal Rahmadani
              <a
                href="https://wa.me/6282254442400"
                target="_blank"
                class="text-xs md:text-lg text-[#646cff] font-medium hover:underline m-0"
                style="text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px;"
              >
                0822-5444-2400
              </a>
            </p>
          </div>
        </div>

        <!-- Kembali -->
        <div class="flex justify-center mt-6">
          <button
            @click="handleKembali"
            class="px-8 md:px-10 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular"
          >
            Kembali
          </button>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>