# 📱 Panduan Responsive Design - PT IMM P2H

Dokumentasi lengkap untuk membuat dan menggunakan komponen responsive pada aplikasi P2H.

---

## 🎯 Tujuan

Aplikasi ini dioptimalkan untuk **mobile-first** karena mayoritas user adalah mobile user. Semua komponen harus responsive dan mudah digunakan di:
- 📱 Mobile (320px - 639px)
- 📱 Large Mobile (640px - 767px)  
- 📱 Tablet (768px - 1023px)
- 💻 Desktop (1024px+)

---

## 🏗️ Struktur Responsive

### 1. Sidebar/Aside (Admin)

**Desktop:**
- Fixed sidebar width: 248px (w-62)
- Always visible
- Scrollable menu items

**Mobile:**
- Hidden by default
- Accessible via hamburger menu di header
- Slide-in dari kiri dengan overlay
- Full screen overlay untuk close

**Cara Pakai:**
```vue
<template>
  <div class="flex">
    <!-- Desktop Sidebar -->
    <div class="hidden lg:block fixed lg:relative w-62 h-screen">
      <Aside :isOpen="true" :onClose="() => {}" />
    </div>
    
    <!-- Mobile Sidebar -->
    <div class="block lg:hidden">
      <Aside :isOpen="isMobileMenuOpen" :onClose="toggleMobileMenu" />
    </div>
    
    <div class="flex-1">
      <HeaderAdmin />
      <!-- Content -->
    </div>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'

const isMobileMenuOpen = ref(false)
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// Provide ke HeaderAdmin untuk hamburger button
provide('toggleMobileMenu', toggleMobileMenu)
</script>
```

---

### 2. Header

**Header Admin:**
- Mobile: Hamburger button (kiri) + Title (center) + Avatar (kanan)
- Tablet: Hamburger + Full title + User info + Avatar
- Desktop: Full title + Date + User info + Avatar

**Header User:**
- Mobile: Logo + Title + Hamburger menu
- Desktop: Logo + Title + Nav links + Logout

**Breakpoints:**
- `lg:hidden` - Show pada mobile/tablet, hide pada desktop
- `hidden lg:block` - Hide pada mobile/tablet, show pada desktop

---

### 3. Cards/Dashboard

Gunakan grid responsive dengan Tailwind:

```vue
<!-- 6 Cards Dashboard -->
<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-1.5 sm:gap-2">
  <ResponsiveCard
    title="Total Kendaraan"
    :value="statisticsData.totalVehicles"
    :icon="UserIcon"
    icon-color="text-black"
    clickable
    @click="openCardDetail('total_vehicles')"
  />
  <!-- More cards... -->
</div>
```

**ResponsiveCard Component:**
```vue
<ResponsiveCard
  title="Judul Card"
  :value="100"
  :icon="IconComponent"
  icon-color="text-blue-600"
  value-color="text-blue-600"
  :clickable="true"
  @click="handleClick"
/>
```

**Breakpoint Grid:**
- Mobile: 2 kolom (`grid-cols-2`)
- Tablet: 3 kolom (`sm:grid-cols-3`)
- Desktop: 6 kolom (`lg:grid-cols-6`)

---

### 4. Tables

**Responsive Table Strategies:**

#### A. Horizontal Scroll (Recommended untuk banyak kolom)
```vue
<div class="overflow-x-auto -mx-3 md:mx-0 md:rounded-lg border-b md:border">
  <table class="w-full border-collapse">
    <thead>
      <tr class="border-b-2 border-gray-400 bg-gray-50">
        <th class="px-2 md:px-4 py-2 md:py-3 text-xs md:text-sm">Tanggal</th>
        <th class="px-2 md:px-4 py-2 md:py-3 text-xs md:text-sm">No. Lambung</th>
        <!-- More columns -->
      </tr>
    </thead>
    <tbody>
      <tr class="border-b hover:bg-gray-50">
        <td class="px-2 md:px-4 py-2 md:py-3 text-xs md:text-sm">{{ data }}</td>
      </tr>
    </tbody>
  </table>
</div>
```

#### B. Hide Columns on Mobile
```vue
<!-- Hide column pada mobile, tampilkan pada desktop -->
<th class="hidden md:table-cell px-4 py-3">Nomor Polisi</th>

<td class="hidden md:table-cell px-4 py-3">{{ item.nomorPolisi }}</td>
```

#### C. Gunakan ResponsiveTable Component
```vue
<ResponsiveTable
  :columns="[
    { key: 'tanggal', label: 'Tanggal', hideOnMobile: false },
    { key: 'noLambung', label: 'No. Lambung', hideOnMobile: false },
    { key: 'nomorPolisi', label: 'Nomor Polisi', hideOnMobile: true },
  ]"
  :data="tableData"
  :loading="isLoading"
  empty-text="Tidak ada data"
>
  <template #cell-hasil="{ value }">
    <span :class="getHasilClass(value)">{{ value }}</span>
  </template>
</ResponsiveTable>
```

---

### 5. Modals

**Responsive Modal:**
```vue
<ResponsiveModal
  :isOpen="modalOpen"
  title="Detail Kendaraan"
  size="large"
  @close="modalOpen = false"
>
  <!-- Modal content -->
  <div>Content here...</div>
  
  <!-- Footer dengan buttons -->
  <template #footer>
    <div class="flex gap-2">
      <button class="flex-1 px-4 py-2 bg-gray-200 rounded">Batal</button>
      <button class="flex-1 px-4 py-2 bg-blue-600 text-white rounded">Simpan</button>
    </div>
  </template>
</ResponsiveModal>
```

**Size Options:**
- `small`: max-w-sm sm:max-w-md
- `medium`: max-w-md sm:max-w-lg md:max-w-xl (default)
- `large`: max-w-lg sm:max-w-xl md:max-w-2xl lg:max-w-4xl
- `full`: max-w-full

**Mobile Behavior:**
- Full width dengan margin 0.5rem
- Max height 90vh untuk scrolling
- Close button tetap visible
- Overlay click untuk close (optional)

---

### 6. Forms

**Responsive Form Best Practices:**

```vue
<form class="space-y-4 md:space-y-6">
  <!-- Single Column Mobile, 2 Columns Desktop -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
    <div>
      <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
        Nama Lengkap
      </label>
      <input
        type="text"
        class="w-full px-3 py-2 text-sm md:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        style="font-size: 16px;" <!-- Prevent iOS zoom -->
      />
    </div>
  </div>
  
  <!-- Full Width Buttons on Mobile -->
  <div class="flex flex-col sm:flex-row gap-2 sm:gap-3">
    <button class="flex-1 px-4 py-2 bg-gray-200 rounded-lg">Batal</button>
    <button class="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg">Simpan</button>
  </div>
</form>
```

**Important:**
- Input `font-size: 16px` untuk prevent zoom di iOS
- Full width buttons pada mobile
- Touch-friendly tap targets (min 44px)

---

## 🎨 Tailwind Responsive Classes

### Display
```
hidden              # Hide semua
block               # Show block
sm:block            # Show block >= 640px
md:hidden           # Hide >= 768px
lg:flex             # Show flex >= 1024px
```

### Grid
```
grid-cols-1         # 1 kolom mobile
sm:grid-cols-2      # 2 kolom >= 640px
md:grid-cols-3      # 3 kolom >= 768px
lg:grid-cols-4      # 4 kolom >= 1024px
xl:grid-cols-6      # 6 kolom >= 1280px
```

### Spacing
```
p-2                 # padding 0.5rem mobile
sm:p-4              # padding 1rem >= 640px
md:p-6              # padding 1.5rem >= 768px

gap-2               # gap 0.5rem mobile
md:gap-4            # gap 1rem >= 768px
```

### Text
```
text-xs             # 12px mobile
sm:text-sm          # 14px >= 640px
md:text-base        # 16px >= 768px
lg:text-lg          # 18px >= 1024px
```

### Width
```
w-full              # 100% width
sm:w-auto           # auto >= 640px
md:w-1/2            # 50% >= 768px
lg:w-1/3            # 33% >= 1024px
```

---

## 📐 Breakpoints Reference

```css
/* Tailwind Default Breakpoints */
/* xs (default) */  0px - 639px     /* Mobile */
/* sm: */           640px - 767px   /* Large Mobile */
/* md: */           768px - 1023px  /* Tablet */
/* lg: */           1024px - 1279px /* Desktop */
/* xl: */           1280px - 1535px /* Large Desktop */
/* 2xl: */          1536px+         /* Extra Large Desktop */
```

---

## ✅ Checklist Responsive

Sebelum push kode, pastikan:

- [ ] Sidebar berfungsi di mobile (hamburger menu)
- [ ] Header responsive dengan semua breakpoints
- [ ] Cards menggunakan responsive grid
- [ ] Tables scrollable horizontal atau hide columns
- [ ] Modals full screen di mobile
- [ ] Forms menggunakan grid responsive
- [ ] Buttons full width di mobile
- [ ] Text size responsive
- [ ] Spacing/padding responsive
- [ ] Test di Chrome DevTools semua ukuran
- [ ] Test di device fisik (mobile, tablet)
- [ ] Meta viewport tag sudah benar
- [ ] Font size input >= 16px (iOS)
- [ ] Touch targets >= 44px
- [ ] No horizontal scroll di mobile (kecuali table)

---

## 🔧 Testing

### Browser DevTools
1. Buka Chrome DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test breakpoints:
   - iPhone SE (375px)
   - iPhone 12 Pro (390px)
   - iPad (768px)
   - iPad Pro (1024px)
4. Test landscape mode
5. Test zoom in/out

### Physical Devices
Test di real devices untuk touch experience:
- Android phone (min 360px width)
- iPhone (min 375px width)
- iPad/Android tablet

---

## 🚀 Tips & Tricks

### 1. Mobile-First Approach
Selalu design mobile dulu, lalu tambahkan breakpoints untuk larger screens:
```vue
<!-- ❌ Bad -->
<div class="lg:grid-cols-6 sm:grid-cols-2">

<!-- ✅ Good -->
<div class="grid-cols-2 sm:grid-cols-3 lg:grid-cols-6">
```

### 2. Prevent iOS Zoom
```vue
<input type="text" style="font-size: 16px;" />
```

### 3. Touch Targets
```css
/* Minimum 44x44px untuk touch */
button, a {
  min-height: 44px;
  min-width: 44px;
}
```

### 4. Negative Margin untuk Full Width
```vue
<!-- Break out dari container padding -->
<div class="-mx-3 md:mx-0">
  <table>...</table>
</div>
```

### 5. Safe Area (iOS Notch)
```css
padding-top: env(safe-area-inset-top);
padding-bottom: env(safe-area-inset-bottom);
```

---

## 📚 Resources

- [Tailwind CSS Responsive Design](https://tailwindcss.com/docs/responsive-design)
- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Web.dev Responsive](https://web.dev/responsive-web-design-basics/)

---

## 📞 Support

Jika ada pertanyaan tentang responsive design, hubungi tim development.

**Last Updated:** 20 Januari 2026
