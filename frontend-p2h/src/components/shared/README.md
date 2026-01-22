# Shared Responsive Components

Komponen reusable untuk membuat UI yang responsive dan konsisten.

## 📦 Components

### 1. ResponsiveTable

Tabel yang otomatis responsive dengan horizontal scroll dan opsi hide columns.

**Props:**
- `columns`: Array - Definisi kolom dengan key, label, hideOnMobile, headerClass
- `data`: Array - Data untuk ditampilkan
- `loading`: Boolean - Status loading
- `emptyText`: String - Text saat data kosong

**Example:**
```vue
<ResponsiveTable
  :columns="[
    { key: 'id', label: 'ID', hideOnMobile: true },
    { key: 'name', label: 'Nama' },
    { key: 'status', label: 'Status' }
  ]"
  :data="tableData"
  :loading="isLoading"
>
  <template #cell-status="{ value }">
    <span :class="getStatusClass(value)">{{ value }}</span>
  </template>
</ResponsiveTable>
```

---

### 2. ResponsiveCard

Card dashboard yang responsive untuk menampilkan statistik.

**Props:**
- `title`: String - Judul card
- `value`: String/Number - Nilai yang ditampilkan
- `icon`: Component - Icon dari Heroicons
- `iconColor`: String - Tailwind class untuk warna icon
- `valueColor`: String - Tailwind class untuk warna value
- `clickable`: Boolean - Apakah card bisa diklik

**Events:**
- `@click` - Emitted saat card diklik (jika clickable=true)

**Example:**
```vue
<ResponsiveCard
  title="Total Kendaraan"
  :value="totalVehicles"
  :icon="TruckIcon"
  icon-color="text-indigo-600"
  value-color="text-indigo-600"
  :clickable="true"
  @click="showDetails"
/>
```

---

### 3. ResponsiveModal

Modal yang full responsive dengan ukuran adaptif.

**Props:**
- `isOpen`: Boolean (required) - Status modal
- `title`: String - Judul modal
- `size`: String - 'small', 'medium', 'large', 'full'
- `showClose`: Boolean - Tampilkan tombol close
- `closeOnOverlay`: Boolean - Close saat klik overlay

**Events:**
- `@close` - Emitted saat modal ditutup

**Slots:**
- `default` - Konten utama modal
- `footer` - Footer modal (optional)

**Example:**
```vue
<ResponsiveModal
  :isOpen="isModalOpen"
  title="Edit Data Kendaraan"
  size="large"
  @close="isModalOpen = false"
>
  <!-- Modal body -->
  <form>...</form>
  
  <!-- Modal footer -->
  <template #footer>
    <div class="flex gap-2">
      <button @click="isModalOpen = false">Batal</button>
      <button @click="saveData">Simpan</button>
    </div>
  </template>
</ResponsiveModal>
```

---

## 🎨 Responsive Features

### Mobile (< 640px)
- Tables: Horizontal scroll, smaller text (text-xs)
- Cards: 2 columns grid
- Modals: Full width dengan padding minimal
- Buttons: Stack vertical

### Tablet (640px - 1023px)
- Cards: 3 columns grid
- Text: Medium size (text-sm)

### Desktop (>= 1024px)
- Full features
- Cards: 6 columns grid (dashboard)
- Text: Normal size (text-base)

---

## 📱 Mobile Optimization

Semua komponen sudah include:
- ✅ Touch-friendly tap targets (min 44px)
- ✅ Prevent iOS zoom (font-size >= 16px)
- ✅ Smooth transitions
- ✅ Loading states
- ✅ Empty states
- ✅ Accessibility support

---

## 🚀 Usage

Import komponen di file yang membutuhkan:

```vue
<script setup>
import ResponsiveTable from '@/components/shared/ResponsiveTable.vue'
import ResponsiveCard from '@/components/shared/ResponsiveCard.vue'
import ResponsiveModal from '@/components/shared/ResponsiveModal.vue'
</script>
```

Atau gunakan auto-import jika sudah dikonfigurasi di vite.config.js.
