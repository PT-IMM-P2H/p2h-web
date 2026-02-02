<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import NavBar from "../bar/header-user.vue";
import Footer from "../bar/footer.vue";
import { InformationCircleIcon } from "@heroicons/vue/24/outline";

const router = useRouter();
const currentDate = ref("");
const submissionData = ref(null);

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

  // Get data from sessionStorage
  const storedData = sessionStorage.getItem("p2hResult");
  if (storedData) {
    try {
      submissionData.value = JSON.parse(storedData);
      // Clear data setelah dibaca untuk mencegah data lama
      sessionStorage.removeItem("p2hResult");
    } catch (error) {
      console.error("Error parsing p2hResult:", error);
      router.push("/form-p2h");
    }
  } else {
    // Jika tidak ada data, redirect ke form
    router.push("/form-p2h");
  }
});

// Computed property untuk status
const isNormal = computed(() => submissionData.value?.status === "normal");
const isAbnormal = computed(() => submissionData.value?.status === "abnormal");
const isWarning = computed(() => submissionData.value?.status === "warning");

const handleWaLink = () => {
  window.open("https://wa.me/6282254442400", "_blank");
};

const handleKembali = () => {
  router.push("/");
};
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <!-- Navbar -->
    <NavBar />

    <!-- Content -->
    <main
      class="flex-1 flex items-center justify-center bg-cover bg-center bg-no-repeat mb-5 pt-20 pb-24 md:pb-16 px-2 md:px-4 overflow-y-auto"
      style="
        background-image: url(/image_asset/BG_2.png);
        background-attachment: fixed;
      "
    >
      <div
        class="p-4 md:p-8 m-2 md:m-3 bg-white rounded-xl shadow-lg w-full max-w-4xl"
      >
        <div class="flex justify-between items-center mb-4">
          <img
            src="/image_asset/2_Ptimm.png"
            alt="Logo"
            class="h-7 md:h-8 w-auto shrink-0"
          />
          <p class="text-xs md:text-sm text-black font-bold">
            {{ currentDate }}
          </p>
        </div>
        <hr class="mt-1 mb-3 border-gray-300" />

        <h1
          class="text-base md:text-xl font-bold mb-1 text-gray-800 text-start"
        >
          Hasil Pelaksanaan Pemeriksaan Harian Kendaraan
        </h1>
        <p class="text-xs text-gray-600 text-left">
          <InformationCircleIcon class="w-3 h-3 inline-block text-gray-500" />
          Form telah disubmit pada {{ submissionData?.submissionTime || "-" }}
        </p>

        <!-- Hasil Normal -->
        <div
          v-if="isNormal"
          class="flex items-start gap-3 mb-2 mt-2 p-2 bg-green-100 border-l-4 border-green-500 rounded"
        >
          <p
            class="text-black font-medium text-sm md:text-base leading-relaxed"
          >
            Kondisi kendaraan : <span class="font-bold">Normal</span>
          </p>
        </div>

        <!-- Pengumuman Box Normal -->
        <div
          v-if="isNormal"
          class="flex items-start gap-3 mb-4 mt-4 p-3 bg-red-50 border-l-4 border-red-500 rounded"
        >
          <div class="text-black font-semibold text-xs leading-relaxed italic">
            <ul class="list-disc list-inside -space-y-0.5">
              <li>Gunakan APD lengkap dan sabuk pengaman</li>
              <li>
                Batas kecepatan:
                <ul class="list-circle list-inside ml-3 -space-y-0.5">
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
          v-if="isAbnormal"
          class="flex items-start gap-3 mb-2 mt-2 p-2 bg-yellow-100 border-l-4 border-yellow-500 rounded"
        >
          <p
            class="text-black font-medium text-sm md:text-base leading-relaxed"
          >
            Kondisi kendaraan : <span class="font-bold">Abnormal</span>
          </p>
        </div>

        <div
          v-if="isAbnormal"
          class="flex items-start gap-3 mb-4 mt-4 p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded"
        >
          <p class="text-black font-semibold text-xs leading-relaxed italic">
            Bagian kendaraan terdapat kerusakan ringan, namun masih dapat
            digunakan dan perlu dilakukan pemeriksaan atau perbaikan di bengkel.
          </p>
        </div>

        <!-- Pengumuman Box Abnormal -->
        <div
          v-if="isAbnormal"
          class="flex items-start gap-3 mb-4 mt-4 p-3 bg-red-50 border-l-4 border-red-500 rounded"
        >
          <div class="text-black font-semibold text-xs leading-relaxed italic">
            <ul class="list-disc list-inside -space-y-0.5">
              <li>Gunakan APD lengkap dan sabuk pengaman</li>
              <li>
                Batas kecepatan:
                <ul class="list-circle list-inside ml-3 -space-y-0.5">
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
          v-if="isWarning"
          class="flex items-start gap-3 mb-2 mt-2 p-2 bg-red-100 border-l-4 border-red-500 rounded"
        >
          <p
            class="text-black font-medium text-sm md:text-base leading-relaxed"
          >
            Kondisi kendaraan : <span class="font-bold">Warning</span>
          </p>
        </div>

        <!-- Pengumuman Box Warning -->
        <div
          v-if="isWarning"
          class="flex items-start gap-3 mb-4 mt-4 p-3 bg-red-50 border-l-4 border-red-500 rounded"
        >
          <div class="text-black font-semibold text-xs leading-relaxed italic">
            <p class="mb-2 font-bold text-sm">
              Bagian kendaraan mengalami kerusakan serius sehingga tidak dapat
              digunakan dan harus segera dibawa ke bengkel untuk penanganan
              lebih lanjut.
            </p>
            <p class="text-red-600 font-bold text-sm mb-2 italic underline">
              <InformationCircleIcon
                class="w-4 h-4 inline-block text-red-600 mr-1"
              />
              Kendaraan dinyatakan tidak dapat dioperasikan
            </p>
            <p class="font-bold text-sm">
              Hubungi Rizal Rahmadani
              <a
                href="https://wa.me/6282254442400"
                target="_blank"
                class="text-xs md:text-sm text-[#646cff] font-medium hover:underline m-0"
                style="
                  text-decoration: underline;
                  text-decoration-thickness: 1px;
                  text-underline-offset: 3px;
                "
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
            class="px-8 md:px-10 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-medium"
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
