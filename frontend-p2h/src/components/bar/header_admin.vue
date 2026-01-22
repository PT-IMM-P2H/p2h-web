<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { UserCircleIcon, Bars3Icon } from '@heroicons/vue/24/outline'
import { useUserProfile } from '../../composables/useUserProfile'
import { useSidebar } from '../../composables/useSidebar'

const router = useRouter()
const route = useRoute()
const currentDate = ref('')

// Use sidebar composable
const { toggleSidebar } = useSidebar()

// Use composable for user profile
const { userProfile, fetchUserProfile, getUserFullName, getUserRoleLabel } = useUserProfile()

const goToProfile = () => {
  router.push('/profil-admin')
}

// Map route paths ke header titles
const routeToHeaderMap = {
  '/form-p2h': 'Formulir P2H',
  '/dashboard': 'Dashboard Pelaksanaan Pemeriksaan Harian',
  '/data-monitor-pt': 'Data Monitor - PT.IMM',
  '/data-monitor-travel': 'Data Monitor - Travel',
  '/data-pengguna-pt': 'Data Pengguna - PT.IMM',
  '/data-pengguna-travel': 'Data Pengguna - Travel',
  '/kelola-pertanyaan': 'Kelola Pertanyaan',
  '/data-perusahaan': 'Master Data - Perusahaan',
  '/data-departemen': 'Master Data - Departemen',
  '/data-posisi': 'Master Data - Posisi',
  '/data-status': 'Master Data - Status Kerja',
  '/unit-kendaraan-pt': 'Unit Kendaraan - PT.IMM',
  '/unit-kendaraan-travel': 'Unit Kendaraan - Travel',
  '/profil-admin': 'Profile Administrator'
}

const headerTitle = computed(() => {
  const currentPath = route.path
  let title = routeToHeaderMap[currentPath]
  
  // Jika route tidak langsung match (misal karena parameter), cek pattern
  if (!title) {
    if (currentPath.match(/^\/edit-data-pengguna-pt\//)) {
      title = 'Edit Data Pengguna - PT.IMM'
    } else if (currentPath.match(/^\/edit-data-pengguna-travel\//)) {
      title = 'Edit Data Pengguna - Travel'
    } else if (currentPath.match(/^\/edit-unit-pt\//)) {
      title = 'Edit Unit Kendaraan - PT.IMM'
    } else if (currentPath.match(/^\/edit-unit-travel\//)) {
      title = 'Edit Unit Kendaraan - Travel'
    } else {
      title = 'Dashboard Pelaksanaan Pemeriksaan Harian' // Default title
    }
  }
  
  return title
})

onMounted(() => {
  // Format tanggal hari ini
  const today = new Date()
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
  currentDate.value = today.toLocaleDateString('id-ID', options)
  
  // Fetch user profile
  fetchUserProfile()
})
</script>

<template>
  <div class="bg-white border-b border-gray-200 px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between sticky top-0 z-50">
    <!-- Burger Menu Button (Mobile/Tablet) -->
    <button 
      @click="toggleSidebar"
      class="lg:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors mr-3 shrink-0"
      aria-label="Toggle menu"
    >
      <Bars3Icon class="w-6 h-6 text-gray-700" />
    </button>
    
    <!-- Left Section - Title & Date -->
    <div class="flex flex-col flex-1 min-w-0">
      <h1 class="text-sm sm:text-base md:text-lg lg:text-xl font-bold text-[#523E95] truncate">{{ headerTitle }}</h1>
      <p class="text-xs text-gray-500 hidden sm:block">{{ currentDate }}</p>
    </div>

    <!-- Right Section - Admin Info -->
    <div class="flex items-center gap-2 sm:gap-4 ml-2">
      <div class="text-right hidden md:block">
        <p class="text-sm md:text-base font-semibold text-gray-800 truncate lg:max-w-none">{{ getUserFullName() }}</p>
        <p class="text-xs text-gray-500 truncate">{{ getUserRoleLabel() }}</p>
      </div>
      <!-- User Circle Icon Button -->
      <button 
        @click="goToProfile"
        aria-label="Buka profil pengguna"
        class="w-8 h-8 sm:w-10 sm:h-10 bg-indigo-100 rounded-full flex items-center justify-center hover:bg-indigo-200 transition-colors duration-200 cursor-pointer shrink-0"
      >
        <UserCircleIcon class="w-8 h-8 sm:w-10 sm:h-10 text-black hover:text-indigo-600 transition-colors duration-200" />
      </button>
    </div>
  </div>
</template>