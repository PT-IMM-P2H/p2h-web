<script setup>
import { defineProps } from 'vue'
import Aside from '../bar/aside.vue'
import HeaderAdmin from '../bar/header_admin.vue'
import { useSidebarProvider } from '../../composables/useSidebar'

defineProps({
  title: {
    type: String,
    default: ''
  }
})

// Setup sidebar state management
const { isSidebarOpen, toggleSidebar, closeSidebar } = useSidebarProvider()
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar - Push content style -->
      <Aside :isOpen="isSidebarOpen" :onClose="closeSidebar" />

      <!-- Main Content Area -->
      <div class="flex flex-col flex-1 min-w-0 overflow-hidden">
        <!-- Header -->
        <HeaderAdmin />

        <!-- Page Content Slot -->
        <main class="bg-[#EFEFEF] flex-1 overflow-y-auto">
          <slot></slot>
        </main>
      </div>
    </div>
  </div>
</template>
