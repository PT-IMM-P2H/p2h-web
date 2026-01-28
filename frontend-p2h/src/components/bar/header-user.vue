<script setup>
import { useRouter } from "vue-router";
import { computed, ref } from "vue";
import { useUserProfile } from "../../composables/useUserProfile";

const router = useRouter();
const isMenuOpen = ref(false);
const { clearProfile, userProfile, fetchUserProfile } = useUserProfile();

const handleLogout = () => {
  // Clear user profile cache
  clearProfile();
  // Clear localStorage token
  localStorage.removeItem("token");
  localStorage.removeItem("access_token"); // Ensure both are cleared if used
  // Redirect to login
  router.push("/login");
  isMenuOpen.value = false;
};

const handleLogin = () => {
  router.push("/login");
  isMenuOpen.value = false;
};

const hadleprofile = () => {
  router.push({ name: "profile-user" });
  isMenuOpen.value = false;
};
const hadlepriwayat = () => {
  router.push({ name: "riwayat-user" });
  isMenuOpen.value = false;
};
const hadleformp2h = () => {
  router.push({ name: "form-p2h" });
  isMenuOpen.value = false;
};

const hadledashboard = () => {
  router.push({ name: "dashboard" });
  isMenuOpen.value = false;
};

const hadlemonitor = () => {
  router.push({ name: "monitor-kendaraan" });
  isMenuOpen.value = false;
};

const hadlehasilP2H = () => {
  router.push({ name: "hasil-form" });
  isMenuOpen.value = false;
};

const currentRoute = computed(() => router.currentRoute.value.name);

const getButtonClass = (routeName) => {
  const isActive = currentRoute.value === routeName;
  return isActive
    ? "text-sm font-bold transition-colors"
    : "text-sm font-light transition-colors";
};

const getButtonColor = (routeName) => {
  const isActive = currentRoute.value === routeName;
  return isActive ? "#523E95" : "#646464";
};

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
  isMenuOpen.value = false;
};

// Check if current route is monitor page
const isMonitorPage = computed(
  () => currentRoute.value === "monitor-kendaraan",
);

// Check if user is authenticated
const isAuthenticated = computed(() => {
  return !!localStorage.getItem("access_token");
});

// Check if user is admin or superadmin
const isAdminAccess = computed(() => {
  const role = userProfile.value?.role;
  return role === "admin" || role === "superadmin";
});

// Fetch profile if authenticated and not loaded
if (isAuthenticated.value && !userProfile.value) {
  fetchUserProfile().catch(() => {
    // Handle error silently or log
  });
}
</script>

<template>
  <header
    class="fixed top-0 left-0 w-full z-50 bg-white/80 backdrop-blur-lg shadow-md px-4 md:px-6 py-3 md:py-4 flex justify-between items-center"
  >
    <div class="flex items-center gap-2 md:gap-3 min-w-0 flex-1">
      <img
        src="/image_asset/2_Ptimm.png"
        alt="Logo"
        class="h-7 md:h-8 w-auto shrink-0"
      />

      <!-- HR vertikal valid -->
      <div class="h-6 md:h-8 w-0.5 bg-[#cacaca] rounded-lg shrink-0"></div>

      <span
        class="font-['Montserrat'] font-semibold text-md md:text-md text-[#523E95] truncate"
      >
        Pelaksanaan Pemeriksaan Harian
      </span>
    </div>

    <!-- Desktop Navigation -->
    <nav class="hidden lg:flex items-center gap-4 xl:gap-6 ml-auto">
      <!-- viewer monitor kendaraan -->
      <button
        @click="hadlemonitor"
        :class="getButtonClass('monitor-kendaraan')"
        :style="{ color: getButtonColor('monitor-kendaraan') }"
        class="text-xs lg:text-sm hover:opacity-70 transition-all duration-200 whitespace-nowrap"
      >
        Log Kendaraan
      </button>

      <!-- User -->
      <button
        v-if="isAuthenticated"
        @click="hadleformp2h"
        :class="getButtonClass('form-p2h')"
        :style="{ color: getButtonColor('form-p2h') }"
        class="text-xs lg:text-sm hover:opacity-70 transition-all duration-200 whitespace-nowrap"
      >
        Form P2H
      </button>
      <button
        v-if="isAuthenticated && isAdminAccess && !isMonitorPage"
        @click="hadlehasilP2H"
        :class="getButtonClass('hasil-form')"
        :style="{ color: getButtonColor('hasil-form') }"
        class="text-xs lg:text-sm hover:opacity-70 transition-all duration-200 whitespace-nowrap"
      >
        Hasil P2H
      </button>
      <button
        v-if="isAuthenticated && !isMonitorPage"
        @click="hadlepriwayat"
        :class="getButtonClass('riwayat-user')"
        :style="{ color: getButtonColor('riwayat-user') }"
        class="text-xs lg:text-sm hover:opacity-70 transition-all duration-200 whitespace-nowrap"
      >
        Riwayat
      </button>
      <button
        v-if="isAuthenticated && !isMonitorPage"
        @click="hadleprofile"
        :class="getButtonClass('profile-user')"
        :style="{ color: getButtonColor('profile-user') }"
        class="text-xs lg:text-sm hover:opacity-70 transition-all duration-200 whitespace-nowrap"
      >
        Profile
      </button>

      <!-- admin -->
      <button
        v-if="isAuthenticated && isAdminAccess && !isMonitorPage"
        @click="hadledashboard"
        :class="getButtonClass('dashboard')"
        :style="{ color: getButtonColor('dashboard') }"
        class="text-xs lg:text-sm hover:opacity-70 transition-all duration-200 whitespace-nowrap"
      >
        Dashboard
      </button>

      <div v-if="isAuthenticated" class="h-5 w-px bg-gray-300"></div>

      <!-- Logout button (only if authenticated) -->
      <button
        v-if="isAuthenticated && !isMonitorPage"
        @click="handleLogout"
        class="text-xs lg:text-sm font-medium text-red-500 hover:text-red-700 transition-all duration-200 whitespace-nowrap"
      >
        Logout
      </button>

      <!-- Login button (only if not authenticated) -->
      <button
        v-if="!isAuthenticated"
        @click="handleLogin"
        class="text-xs lg:text-sm font-medium text-blue-600 hover:text-blue-800 transition-all duration-200 whitespace-nowrap"
      >
        Login
      </button>
    </nav>

    <!-- Mobile Hamburger Button -->
    <button
      @click="toggleMenu"
      class="lg:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors duration-200 ml-auto"
    >
      <div v-if="!isMenuOpen" class="space-y-1.5">
        <div class="w-5 h-0.5 bg-[#523E95] transition-all duration-300"></div>
        <div class="w-5 h-0.5 bg-[#523E95] transition-all duration-300"></div>
        <div class="w-5 h-0.5 bg-[#523E95] transition-all duration-300"></div>
      </div>
      <div v-else class="text-xl text-[#523E95] font-bold">✕</div>
    </button>
  </header>

  <!-- Mobile Menu -->
  <transition
    enter-active-class="transition ease-out duration-200"
    enter-from-class="opacity-0 -translate-y-1"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition ease-in duration-150"
    leave-from-class="opacity-100 translate-y-0"
    leave-to-class="opacity-0 -translate-y-1"
  >
    <nav
      v-if="isMenuOpen"
      class="lg:hidden fixed top-16 left-0 w-full bg-white/95 backdrop-blur-lg shadow-md z-40 border-b border-gray-200"
    >
      <div class="px-4 py-3 space-y-1">
        <button
          v-if="isAuthenticated"
          @click="hadleformp2h"
          :class="getButtonClass('form-p2h')"
          :style="{ color: getButtonColor('form-p2h') }"
          class="block w-full text-left px-3 py-2.5 text-sm rounded-md hover:bg-gray-50 transition-colors duration-200"
        >
          Form P2H
        </button>
        <button
          v-if="isAuthenticated && isAdminAccess && !isMonitorPage"
          @click="hadlehasilP2H"
          :class="getButtonClass('hasil-form')"
          :style="{ color: getButtonColor('hasil-form') }"
          class="block w-full text-left px-3 py-2.5 text-sm rounded-md hover:bg-gray-50 transition-colors duration-200"
        >
          Hasil P2H
        </button>
        <button
          v-if="isAuthenticated && !isMonitorPage"
          @click="hadlepriwayat"
          :class="getButtonClass('riwayat-user')"
          :style="{ color: getButtonColor('riwayat-user') }"
          class="block w-full text-left px-3 py-2.5 text-sm rounded-md hover:bg-gray-50 transition-colors duration-200"
        >
          Riwayat
        </button>
        <button
          v-if="isAuthenticated && !isMonitorPage"
          @click="hadleprofile"
          :class="getButtonClass('profile-user')"
          :style="{ color: getButtonColor('profile-user') }"
          class="block w-full text-left px-3 py-2.5 text-sm rounded-md hover:bg-gray-50 transition-colors duration-200"
        >
          Profile
        </button>
        <button
          @click="hadlemonitor"
          :class="getButtonClass('monitor-kendaraan')"
          :style="{ color: getButtonColor('monitor-kendaraan') }"
          class="block w-full text-left px-3 py-2.5 text-sm rounded-md hover:bg-gray-50 transition-colors duration-200"
        >
          Log Kendaraan
        </button>
        <button
          v-if="isAuthenticated && isAdminAccess && !isMonitorPage"
          @click="hadledashboard"
          :class="getButtonClass('dashboard')"
          :style="{ color: getButtonColor('dashboard') }"
          class="block w-full text-left px-3 py-2.5 text-sm rounded-md hover:bg-gray-50 transition-colors duration-200"
        >
          Dashboard
        </button>
        <hr v-if="isAuthenticated" class="border-gray-200 my-2" />

        <!-- Logout (only if authenticated) -->
        <button
          v-if="isAuthenticated && !isMonitorPage"
          @click="handleLogout"
          class="block w-full text-left px-3 py-2.5 text-sm font-medium text-red-500 rounded-md hover:bg-red-50 hover:text-red-700 transition-colors duration-200"
        >
          Logout
        </button>

        <!-- Login (only if not authenticated) -->
        <button
          v-if="!isAuthenticated"
          @click="handleLogin"
          class="block w-full text-left px-3 py-2.5 text-sm font-medium text-blue-600 rounded-md hover:bg-blue-50 hover:text-blue-800 transition-colors duration-200"
        >
          Login
        </button>
      </div>
    </nav>
  </transition>
</template>
