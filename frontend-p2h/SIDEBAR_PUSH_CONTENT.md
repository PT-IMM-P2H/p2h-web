# 📱 Update Responsive - Sidebar Push Content

## ✅ Perubahan Terbaru

### Sidebar Behavior Baru:
- ✅ **Burger Menu** (3 garis horizontal) di header
- ✅ **Push Content** - Sidebar mendorong konten, bukan menutupi
- ✅ Smooth animation saat buka/tutup
- ✅ Desktop: Sidebar always visible
- ✅ Mobile/Tablet: Sidebar collapsible dengan width animation

---

## 🎯 Cara Kerja

### Desktop (>= 1024px)
- Sidebar **selalu visible** dengan width 248px
- Burger menu **hidden**
- Content auto-adjust

### Mobile/Tablet (< 1024px)
- Sidebar **width: 0** saat closed (hidden)
- Sidebar **width: 248px** saat open
- Content **geser ke kanan** saat sidebar open
- Burger menu **visible** di header

---

## 🔧 Implementasi

### 1. Gunakan Composable (Recommended)

**File:** `src/composables/useSidebar.js`

```vue
<script setup>
import Aside from "../bar/aside.vue"
import HeaderAdmin from "../bar/header_admin.vue"
import { useSidebarProvider } from "../../composables/useSidebar"

// Setup sidebar state
const { isSidebarOpen, closeSidebar } = useSidebarProvider()
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Montserrat']">
    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <Aside :isOpen="isSidebarOpen" :onClose="closeSidebar" />

      <!-- Main Content -->
      <div class="flex flex-col flex-1 min-w-0 overflow-hidden">
        <HeaderAdmin />
        
        <main class="bg-[#EFEFEF] flex-1 overflow-y-auto p-4">
          <!-- Your content here -->
        </main>
      </div>
    </div>
  </div>
</template>
```

### 2. Gunakan Layout Component (Lebih Simple)

**File:** `src/components/layouts/AdminLayout.vue`

```vue
<script setup>
import AdminLayout from '@/components/layouts/AdminLayout.vue'
</script>

<template>
  <AdminLayout title="Dashboard">
    <!-- Your content here -->
    <div class="p-4">
      <h1>Dashboard Content</h1>
    </div>
  </AdminLayout>
</template>
```

---

## 📁 File yang Diupdate

### Core Files:
1. ✅ `src/components/bar/aside.vue` - Sidebar dengan width animation
2. ✅ `src/components/bar/header_admin.vue` - Burger menu button
3. ✅ `src/composables/useSidebar.js` - State management (BARU)
4. ✅ `src/components/layouts/AdminLayout.vue` - Layout wrapper (BARU)
5. ✅ `src/components/admin/dashboard.vue` - Updated implementation

### Components yang Perlu Update:
- `src/components/admin/kelola-pertanyaan.vue`
- `src/components/admin/profil-admin.vue`
- `src/components/admin/data_monitor/*.vue`
- `src/components/admin/data_pengguna/*.vue`
- `src/components/admin/master_data/*.vue`
- `src/components/admin/unit-kendaraan/*.vue`

---

## 🎨 Cara Sidebar Bekerja

### CSS Classes Breakdown:

```vue
<!-- Aside Component -->
<aside :class="[
  'h-screen bg-white ...',
  // Desktop: always visible, fixed width
  'lg:relative lg:w-62',
  // Mobile: collapsible
  isOpen ? 'w-62 sm:w-72' : 'w-0 lg:w-62'
]">
```

**Penjelasan:**
- `w-0` → Sidebar width 0 (hidden) saat closed di mobile
- `w-62` → Sidebar width 248px saat open di mobile
- `lg:w-62` → Sidebar always 248px di desktop
- `transition-all duration-300` → Smooth animation

### Content Wrapper:

```vue
<div class="flex flex-1 overflow-hidden">
  <Aside /> <!-- Width: 0 or 248px -->
  <div class="flex-1 min-w-0"> <!-- Flex-1 auto adjust width -->
    <!-- Content geser otomatis -->
  </div>
</div>
```

---

## 🚀 Migration Guide

### Before (Old):
```vue
<script setup>
import { ref, provide } from 'vue'

const isMobileMenuOpen = ref(false)
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
provide('toggleMobileMenu', toggleMobileMenu)
</script>

<template>
  <div class="hidden lg:block">
    <Aside :isOpen="true" />
  </div>
  <div class="lg:hidden">
    <Aside :isOpen="isMobileMenuOpen" :onClose="toggleMobileMenu" />
  </div>
</template>
```

### After (New):
```vue
<script setup>
import { useSidebarProvider } from '@/composables/useSidebar'

const { isSidebarOpen, closeSidebar } = useSidebarProvider()
</script>

<template>
  <div class="flex overflow-hidden">
    <Aside :isOpen="isSidebarOpen" :onClose="closeSidebar" />
    <div class="flex-1">
      <!-- Content -->
    </div>
  </div>
</template>
```

---

## 🎯 Benefits

### 1. **Better UX**
- ✅ Content tidak tertutup sidebar
- ✅ Jelas berapa lebar content area
- ✅ Smooth animation

### 2. **Cleaner Code**
- ✅ Centralized state management
- ✅ Reusable composable
- ✅ Konsisten di semua halaman

### 3. **Mobile-Friendly**
- ✅ Touch-friendly burger button
- ✅ Clear visual feedback
- ✅ No overlay confusion

---

## 🧪 Testing

### Mobile (< 640px):
1. Sidebar hidden by default (width: 0)
2. Click burger → sidebar slide in (width: 248px)
3. Content geser ke kanan
4. Click outside atau close → sidebar slide out

### Tablet (640px - 1023px):
1. Sidebar hidden by default
2. Click burger → sidebar width 288px (sm:w-72)
3. Content geser proportional

### Desktop (>= 1024px):
1. Sidebar always visible (width: 248px)
2. Burger button hidden
3. Content width auto-adjust

---

## 📝 Notes

- **No Overlay**: Sidebar tidak pakai overlay hitam, lebih clean
- **Smooth Transition**: `transition-all duration-300 ease-in-out`
- **Overflow Hidden**: Parent container pakai `overflow-hidden` untuk smooth animation
- **Min Width 0**: Content wrapper pakai `min-w-0` untuk prevent flex overflow

---

## 🎨 Animation Details

```css
/* Sidebar Animation */
transition-all duration-300 ease-in-out

/* Properties yang berubah: */
- width: 0 → 248px (mobile/tablet)
- opacity: 0 → 100 (content inside)

/* Content Animation */
- width: auto adjust by flexbox
- smooth reflow
```

---

## 🐛 Troubleshooting

### Issue: Content tidak geser
**Solution:** Pastikan parent container pakai `flex` dan content pakai `flex-1`

### Issue: Sidebar text terpotong saat animasi
**Solution:** Sidebar content wrapper pakai `opacity` transition

### Issue: Burger button tidak muncul
**Solution:** Pastikan import `useSidebar` di header_admin

### Issue: Sidebar tidak responsive
**Solution:** Check classes: `isOpen ? 'w-62' : 'w-0 lg:w-62'`

---

**Updated:** 20 Januari 2026  
**Status:** ✅ Production Ready
