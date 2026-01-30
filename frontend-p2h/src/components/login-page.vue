<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/solid";
import { PhoneIcon } from "@heroicons/vue/24/outline";
import { api } from "../services/api";
import { STORAGE_KEYS } from "../constants";

const router = useRouter();
const showPassword = ref(false);
const showForgotPasswordModal = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const openForgotPasswordModal = () => {
  showForgotPasswordModal.value = true;
};

const closeForgotPasswordModal = () => {
  showForgotPasswordModal.value = false;
};

const phoneNumber = ref("");
const password = ref("");
const loading = ref(false);
const errorMessage = ref("");

const handleSignIn = async (event) => {
  if (event) event.preventDefault();

  if (!phoneNumber.value || !password.value) {
    errorMessage.value = "Nomor HP dan Password harus diisi";
    return;
  }

  try {
    loading.value = true;
    errorMessage.value = "";

    // OAuth2PasswordRequestForm mengharapkan username dan password sebagai form data
    const formData = new FormData();
    formData.append("username", phoneNumber.value);
    formData.append("password", password.value);

    const response = await api.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    console.log("Login response:", response.data);

    // Backend menggunakan status: 'success' bukan success: true
    if (response.data.status === "success" && response.data.payload) {
      const { access_token, user } = response.data.payload;

      console.log("User data:", user);
      console.log("User role:", user.role);

      // Simpan token dan user data ke localStorage
      localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, access_token);
      localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
      localStorage.setItem("user_role", user.role); // Untuk router guard

      // Redirect berdasarkan role
      if (user.role === "superadmin" || user.role === "admin") {
        console.log("Redirecting to dashboard...");
        await router.push("/dashboard");
      } else {
        console.log("Redirecting to form-p2h...");
        await router.push("/form-p2h");
      }
    }
  } catch (error) {
    console.error("Login error:", error);
    errorMessage.value =
      error.response?.data?.detail || "Nomor HP atau Password salah";
  } finally {
    loading.value = false;
  }
};

const handleMonitorKendaraan = () => {
  router.push("/monitor-kendaraan");
};

const handleWaLink = () => {
  window.open("https://wa.me/6282254442400", "_blank");
};
</script>

<template>
  <div
    class="fixed inset-0 flex items-center justify-center bg-cover bg-center font-sans"
    style="background-image: url(&quot;image_asset/BG_2.png&quot;)"
  >
    <div
      class="w-105 h-auto bg-white rounded-[15px] flex items-center justify-center p-2.5 m-2.5 shadow-[0_8px_32px_rgba(0,0,0,0.2),0_2px_8px_rgba(0,0,0,0.15)]"
    >
      <div class="w-full px-7.5 py-5 flex flex-col gap-3.75">
        <img
          src="/image_asset/IMM.svg"
          alt="Logo PT Indominco Mandiri"
          class="w-37.5 h-auto block mx-auto"
        />

        <p
          class="m-0 mb-1 mt-3 leading-tight text-center text-black text-[14px] font-sans font-medium mx-auto"
        >
          Pelaksanaan Pemeriksaan Harian Kendaraan Operasional PT Indominco
          Mandiri
        </p>

        <!-- Login Form -->
        <form @submit="handleSignIn" class="flex flex-col gap-3.75">
          <!-- Phone -->
          <div class="flex flex-col">
            <input
              id="phone_number"
              name="phone_number"
              v-model="phoneNumber"
              type="tel"
              placeholder="Nomor Handphone"
              autocomplete="tel"
              class="px-3.75 py-3 border border-[#a1a1a1] bg-white rounded-lg text-[14px] text-[#333] transition-colors duration-300 focus:outline-none focus:border-[#646cff] focus:ring-3 focus:ring-[#646cff]/10"
            />
          </div>

          <!-- Password -->
          <div class="relative flex flex-col">
            <input
              id="password"
              name="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Password"
              autocomplete="current-password"
              class="px-3.75 py-3 border border-[#a1a1a1] bg-white rounded-lg text-[14px] text-[#333] transition-colors duration-300 focus:outline-none focus:border-[#646cff] focus:ring-3 focus:ring-[#646cff]/10"
            />
            <button
              type="button"
              @click="togglePasswordVisibility"
              :aria-label="
                showPassword ? 'Sembunyikan password' : 'Tampilkan password'
              "
              class="absolute right-3 top-1/2 -translate-y-1/2 bg-none border-none p-0 cursor-pointer w-5 h-5 flex items-center justify-center transition-all duration-300 hover:opacity-70"
            >
              <EyeIcon
                v-if="showPassword"
                class="w-5 h-5 text-[#646cff] hover:text-[#535bf2]"
              />
              <EyeSlashIcon
                v-else
                class="w-5 h-5 text-[#646cff] hover:text-[#535bf2]"
              />
            </button>
          </div>

          <!-- Error Message -->
          <div
            v-if="errorMessage"
            class="p-3 bg-red-50 border-l-4 border-red-500 rounded"
          >
            <p class="text-red-700 text-sm">{{ errorMessage }}</p>
          </div>

          <!-- Forgot -->
          <div class="flex justify-end mb-2.5">
            <a
              @click.prevent="openForgotPasswordModal"
              class="text-[13px] font-semibold text-[#646cff] transition-colors duration-300 hover:text-[#535bf2] hover:underline cursor-pointer"
            >
              Lupa Password?
            </a>
          </div>

          <!-- Sign In -->
          <div class="flex justify-center">
            <button
              type="submit"
              :disabled="loading"
              class="w-fit px-25 py-3 bg-[#523E95] text-white rounded-xl text-[16px] font-semilight cursor-pointer transition-colors duration-300 hover:bg-[#43317d] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? "Memproses..." : "Masuk" }}
            </button>
          </div>
        </form>

        <hr class="border-t-3 border-[#b7b7b7] rounded-lg m-0.5" />

        <!-- Monitor -->
        <div class="flex justify-center">
          <button
            @click="handleMonitorKendaraan"
            class="w-fit px-14 py-3 bg-[#4A91D7] text-white rounded-xl text-[16px] font-semilight cursor-pointer transition-colors duration-300 hover:bg-[#397cc0]"
          >
            Monitor kendaraan
          </button>
        </div>

        <p
          class="m-0 mt-0 text-left text-[#ff6464] text-[12px] font-bold underline"
        >
          *Notes : Anda dapat mengakses monitor kendaraan tanpa perlu login
        </p>
      </div>
    </div>

    <!-- Forgot Password -->
    <div
      v-if="showForgotPasswordModal"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-1000"
    >
      <div
        class="bg-white p-10 rounded-lg text-center max-w-130 m-2.5 shadow-[0_4px_6px_rgba(0,0,0,0.1)]"
      >
        <h3
          class="text-[#333] text-[17px] font-regular mb-5 leading-normal text-left mt-0"
        >
          Silahkan hubungi Admin Transportasi Manajemen IMM agar kami dapat
          memberikan informasi lebih lanjut tentang password anda.
        </h3>

        <p
          class="text-[#333] text-[16px] mb-5 leading-normal text-left mt-5 flex items-center gap-3"
        >
          <PhoneIcon class="shrink-0 w-5 h-5 text-[#3b82f6]" />
          <span class="font-bold"> Rizal Rahmadani :</span>
          <a
            href="#"
            @click.prevent="handleWaLink"
            class="text-[#646cff] text-[16px] font-medium underline decoration-1"
            style="
              text-decoration: underline;
              text-decoration-thickness: 1.2px;
              text-underline-offset: 3px;
            "
          >
            0822-5444-2400
          </a>
        </p>

        <button
          @click="closeForgotPasswordModal"
          class="px-7.5 py-3 mt-2.5 bg-[#646cff] text-white border-none rounded-md text-[16px] font-semibold cursor-pointer transition-colors duration-300 hover:bg-[#535bf2]"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>
