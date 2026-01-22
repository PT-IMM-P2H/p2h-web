<script setup>
import { ref, computed } from "vue";
import Aside from "../../bar/aside.vue";
import HeaderAdmin from "../../bar/header_admin.vue";
import { useSidebarProvider } from "../../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <div class="flex flex-1 overflow-hidden">
      <Aside />
      <div class="flex flex-col flex-1 overflow-hidden">
        <HeaderAdmin />
        
        <!-- Content -->
        <div class="bg-[#EFEFEF] flex-1 flex flex-col p-3 overflow-hidden">
          <main>

          </main>
        </div>
      </div>
    </div>
  </div>
</template>
