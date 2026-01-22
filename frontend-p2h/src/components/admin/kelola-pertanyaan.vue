<script setup>
import { ref, onMounted } from "vue";
import Aside from "../bar/aside.vue";
import HeaderAdmin from "../bar/header_admin.vue";
import VehicleTypeListModal from "./VehicleTypeListModal.vue";
import VehicleTypeModal from "./VehicleTypeModal.vue";
import {
  DocumentPlusIcon,
  TrashIcon,
  XMarkIcon,
  CheckIcon,
  PlusIcon,
  WrenchIcon,
} from "@heroicons/vue/24/outline";
import { PencilIcon, ChevronDownIcon } from "@heroicons/vue/24/solid";
import { api } from "../../services/api";
import { useSidebarProvider } from "../../composables/useSidebar";

// Provide sidebar state untuk header dan aside
const { isSidebarOpen } = useSidebarProvider();

const tambahPertanyaan = ref(false);
const editPertanyaan = ref(false);
const editingPertanyaan = ref(null);
const selectedRows = ref([]);
const loading = ref(false);
const confirmDelete = ref(false);
const pertanyaanToDelete = ref(null);

// Vehicle Types Management
const vehicleTypeListModal = ref(false);
const vehicleTypeModal = ref(false);
const vehicleTypeEditMode = ref(false);
const vehicleTypeLoading = ref(false);
const currentVehicleType = ref(null);

const formPertanyaan = ref("");

const formJawabanList = ref([
  {
    id: 1,
    jawaban: "",
    pilihan: "",
  },
]);

const pertanyaanList = ref([]);

const openEditPertanyaan = (pertanyaan) => {
  editingPertanyaan.value = JSON.parse(JSON.stringify(pertanyaan));
  editPertanyaan.value = true;
  formPertanyaan.value = pertanyaan.pertanyaan;
  formJawabanList.value = JSON.parse(JSON.stringify(pertanyaan.jawabanList));
  vehicleTypes.value = JSON.parse(JSON.stringify(pertanyaan.vehicleTypes));
};

const closeEditPertanyaan = () => {
  editPertanyaan.value = false;
  editingPertanyaan.value = null;
  formPertanyaan.value = "";
  formJawabanList.value = [
    {
      id: 1,
      jawaban: "",
      pilihan: "",
    },
  ];
  vehicleTypes.value = vehicleList.value.reduce((acc, vehicle) => {
    acc[vehicle.id] = false;
    return acc;
  }, {});
};

const simpanEditPertanyaan = async () => {
  if (editingPertanyaan.value && formPertanyaan.value.trim()) {
    const jawabanList = formJawabanList.value.filter(
      (form) => form.jawaban && form.pilihan
    );

    if (jawabanList.length > 0) {
      try {
        loading.value = true;
        
        // Convert vehicleTypes object ke array tags
        const selectedTags = vehicleList.value
          .filter(v => vehicleTypes.value[v.id])
          .map(v => v.tag);
        
        const payload = {
          question_text: formPertanyaan.value,
          section_name: editingPertanyaan.value.section_name || "UMUM",
          vehicle_tags: selectedTags,
          applicable_shifts: ["Shift 1", "Shift 2"],
          options: jawabanList.map(j => `${j.jawaban}|${j.pilihan}`),
          item_order: editingPertanyaan.value.item_order || 1
        };
        
        const response = await api.put(`/p2h/checklist/${editingPertanyaan.value.id}`, payload);
        
        if (response.data.status === "success") {
          await fetchPertanyaan(); // Reload data
          closeEditPertanyaan();
        }
      } catch (error) {
        console.error("Error updating pertanyaan:", error);
        alert("Gagal mengupdate pertanyaan: " + (error.response?.data?.detail || error.message));
      } finally {
        loading.value = false;
      }
    }
  }
};

const opentambahPertanyaan = () => {
  tambahPertanyaan.value = true;
};

const closetambahPertanyaan = () => {
  tambahPertanyaan.value = false;
  formPertanyaan.value = "";
  formJawabanList.value = [
    {
      id: 1,
      jawaban: "",
      pilihan: "",
    },
  ];
  vehicleTypes.value = vehicleList.value.reduce((acc, vehicle) => {
    acc[vehicle.id] = false;
    return acc;
  }, {});
};

// Dynamic vehicle types from API
const vehicleList = ref([]);
const vehicleTypes = ref({});

// Fetch vehicle types from API
const fetchVehicleTypes = async () => {
  try {
    const response = await api.get('/vehicle-types/active');
    if (response.data.status === 'success') {
      const types = response.data.payload;
      vehicleList.value = types.map(type => ({
        id: type.id,
        label: type.name,
        tag: type.name,
        description: type.description
      }));
      
      // Initialize vehicleTypes object
      vehicleTypes.value = vehicleList.value.reduce((acc, vehicle) => {
        acc[vehicle.id] = false;
        return acc;
      }, {});
    }
  } catch (error) {
    console.error('Error fetching vehicle types:', error);
    alert('Gagal memuat tipe kendaraan');
  }
};

// Fetch all vehicle types for management modal
const allVehicleTypes = ref([]);
const fetchAllVehicleTypes = async () => {
  try {
    vehicleTypeLoading.value = true;
    const response = await api.get('/vehicle-types?limit=1000');
    if (response.data.status === 'success') {
      allVehicleTypes.value = response.data.payload.items;
    }
  } catch (error) {
    console.error('Error fetching all vehicle types:', error);
    alert('Gagal memuat daftar tipe kendaraan');
  } finally {
    vehicleTypeLoading.value = false;
  }
};

// Open vehicle type management modal
const openVehicleTypeList = async () => {
  await fetchAllVehicleTypes();
  vehicleTypeListModal.value = true;
};

// Add new vehicle type
const handleAddVehicleType = () => {
  vehicleTypeEditMode.value = false;
  currentVehicleType.value = null;
  vehicleTypeModal.value = true;
};

// Edit vehicle type
const handleEditVehicleType = (vehicleType) => {
  vehicleTypeEditMode.value = true;
  currentVehicleType.value = vehicleType;
  vehicleTypeModal.value = true;
};

// Submit vehicle type (create or update)
const handleVehicleTypeSubmit = async (formData) => {
  try {
    vehicleTypeLoading.value = true;
    
    if (vehicleTypeEditMode.value && currentVehicleType.value) {
      // Update existing
      const response = await api.put(`/vehicle-types/${currentVehicleType.value.id}`, formData);
      if (response.data.status === 'success') {
        alert('Tipe kendaraan berhasil diupdate!');
        // Refresh both lists in parallel for better performance
        await Promise.all([
          fetchAllVehicleTypes(),
          fetchVehicleTypes()
        ]);
        vehicleTypeModal.value = false;
      }
    } else {
      // Create new
      const response = await api.post('/vehicle-types', formData);
      if (response.data.status === 'success') {
        alert('Tipe kendaraan berhasil ditambahkan!');
        // Refresh both lists in parallel for better performance
        await Promise.all([
          fetchAllVehicleTypes(),
          fetchVehicleTypes()
        ]);
        vehicleTypeModal.value = false;
      }
    }
  } catch (error) {
    console.error('Error saving vehicle type:', error);
    
    // Extract error message
    let errorMessage = 'Gagal menyimpan tipe kendaraan';
    
    if (error.response) {
      // Handle different error statuses
      if (error.response.status === 409) {
        errorMessage = error.response.data?.message || 'Nama tipe kendaraan sudah ada. Gunakan nama yang berbeda.';
      } else if (error.response.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail;
      }
    } else {
      errorMessage += ': ' + error.message;
    }
    
    alert(errorMessage);
  } finally {
    vehicleTypeLoading.value = false;
  }
};

// Delete vehicle type
const handleDeleteVehicleType = async (vehicleType) => {
  if (confirm(`Apakah Anda yakin ingin menghapus tipe kendaraan "${vehicleType.name}"?`)) {
    try {
      vehicleTypeLoading.value = true;
      const response = await api.delete(`/vehicle-types/${vehicleType.id}`);
      if (response.data.status === 'success') {
        alert('Tipe kendaraan berhasil dihapus!');
        // Refresh both lists in parallel for better performance
        await Promise.all([
          fetchAllVehicleTypes(),
          fetchVehicleTypes()
        ]);
      }
    } catch (error) {
      console.error('Error deleting vehicle type:', error);
      alert('Gagal menghapus tipe kendaraan: ' + (error.response?.data?.detail || error.message));
    } finally {
      vehicleTypeLoading.value = false;
    }
  }
};

// Fetch data dari backend
const fetchPertanyaan = async () => {
  try {
    loading.value = true;
    const response = await api.get("/p2h/checklist-items");
    if (response.data.status === "success") {
      // Transform backend data ke format frontend
      pertanyaanList.value = response.data.payload.map(item => ({
        id: item.id,
        pertanyaan: item.item_name,
        section_name: item.section_name,
        vehicleTypes: vehicleList.value.reduce((acc, vehicle) => {
          acc[vehicle.id] = item.vehicle_tags.includes(vehicle.tag);
          return acc;
        }, {}),
        jawabanList: item.options.map((opt, idx) => {
          const [jawaban, pilihan] = opt.includes('|') ? opt.split('|') : [opt, ''];
          return {
            id: idx + 1,
            jawaban: jawaban,
            pilihan: pilihan
          };
        }),
        item_order: item.item_order
      }));
    }
  } catch (error) {
    console.error("Error fetching pertanyaan:", error);
  } finally {
    loading.value = false;
  }
};

// Load data saat component mounted
onMounted(async () => {
  await fetchVehicleTypes(); // Load vehicle types first and wait
  await fetchPertanyaan(); // Then load pertanyaan after vehicleList is populated
});

const hapusPertanyaan = (pertanyaan) => {
  pertanyaanToDelete.value = pertanyaan;
  confirmDelete.value = true;
};

const konfirmasiHapus = async () => {
  if (pertanyaanToDelete.value) {
    try {
      loading.value = true;
      const response = await api.delete(`/p2h/checklist/${pertanyaanToDelete.value.id}`);
      
      if (response.data.status === "success") {
        await fetchPertanyaan(); // Reload data
        confirmDelete.value = false;
        pertanyaanToDelete.value = null;
      }
    } catch (error) {
      console.error("Error deleting pertanyaan:", error);
      alert("Gagal menghapus pertanyaan: " + (error.response?.data?.detail || error.message));
    } finally {
      loading.value = false;
    }
  }
};

const batalHapus = () => {
  confirmDelete.value = false;
  pertanyaanToDelete.value = null;
};

const tambahKontainerPertanyaan = () => {
  const newId = Math.max(...formJawabanList.value.map((p) => p.id), 0) + 1;
  formJawabanList.value.push({
    id: newId,
    jawaban: "",
    pilihan: "",
  });
};

const simpanPertanyaan = async () => {
  if (formPertanyaan.value.trim()) {
    const jawabanList = formJawabanList.value.filter(
      (form) => form.jawaban && form.pilihan
    );

    if (jawabanList.length > 0) {
      try {
        loading.value = true;
        
        // Convert vehicleTypes object ke array tags
        const selectedTags = vehicleList.value
          .filter(v => vehicleTypes.value[v.id])
          .map(v => v.tag);
        
        const payload = {
          question_text: formPertanyaan.value,
          section_name: "UMUM", // Default section, bisa ditambahkan input
          vehicle_tags: selectedTags,
          applicable_shifts: ["Shift 1", "Shift 2"], // Default, bisa ditambahkan input
          options: jawabanList.map(j => `${j.jawaban}|${j.pilihan}`),
          item_order: pertanyaanList.value.length + 1
        };
        
        const response = await api.post("/p2h/checklist", payload);
        
        if (response.data.status === "success") {
          await fetchPertanyaan(); // Reload data
          closetambahPertanyaan();
        }
      } catch (error) {
        console.error("Error saving pertanyaan:", error);
        alert("Gagal menyimpan pertanyaan: " + (error.response?.data?.detail || error.message));
      } finally {
        loading.value = false;
      }
    }
  }
};
</script>

<template>
  <!-- ROOT -->
  <div class="h-screen flex flex-col font-['Montserrat'] overflow-hidden">
    <div class="flex flex-1 min-h-0 overflow-hidden">
      <Aside />

      <!-- CONTENT -->
      <div class="flex flex-col flex-1 min-h-0 overflow-hidden">
        <HeaderAdmin class="shrink-0" />

        <!-- Content -->
        <main
          class="bg-[#EFEFEF] flex-1 flex flex-col p-3 min-h-0 overflow-hidden"
        >
          <div
            class="bg-white rounded-lg shadow-md p-5 flex-1 flex flex-col min-h-0 overflow-hidden"
          >
            <!-- Header konten -->
            <div
              class="flex items-center gap-3 border-b shrink-0 justify-between pb-4"
            >
              <div class="flex items-center gap-3">
                <button
                  @click="opentambahPertanyaan"
                  class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-white bg-[#6444C6] hover:bg-[#5c3db8] transition text-sm"
                >
                  <DocumentPlusIcon class="w-5 h-5" />
                  <span>Tambah Pertanyaan</span>
                </button>
                
                <!-- Button Kelola Tipe Kendaraan -->
                <button
                  @click="openVehicleTypeList"
                  class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50 transition text-sm"
                >
                  <WrenchIcon class="w-5 h-5" />
                  <span>Kelola Tipe Kendaraan</span>
                </button>
              </div>
            </div>

            <!-- ===== SCROLL DIMULAI DI SINI ===== -->
            <div
              class="flex-1 flex flex-col w-full bg-gray-50 rounded-lg border border-gray-200 min-h-0 overflow-hidden mt-4"
            >
              <div
                class="flex-1 flex flex-col w-full gap-4 overflow-y-auto p-4 min-h-0"
              >
                <!-- KONTEN TIDAK DIUBAH -->
                <div
                  v-for="pertanyaan in pertanyaanList"
                  :key="pertanyaan.id"
                  class="flex flex-col w-full bg-white rounded-lg border border-gray-200 shrink-0"
                >
                  <div class="px-4 pb-4">
                    <div>
                      <div class="flex justify-between items-center mb-2 mt-4">
                        <label class="text-lg font-bold text-black"
                          >Tipe kendaraan</label
                        >
                        <div class="flex items-center gap-3">
                          <button
                            @click="openEditPertanyaan(pertanyaan)"
                            class="px-4 md:px-8 py-2 text-sm bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition"
                          >
                            Edit
                          </button>
                          <button
                            @click="hapusPertanyaan(pertanyaan)"
                            class="px-4 md:px-8 py-2 text-sm bg-red-600 text-white rounded-xl hover:bg-red-700 transition"
                          >
                            Hapus
                          </button>
                        </div>
                      </div>
                      <div class="flex flex-wrap gap-2">
                        <span
                          v-for="vehicle in (vehicleList || []).filter(v => pertanyaan.vehicleTypes[v.id])"
                          :key="vehicle.id"
                          class="inline-flex items-center gap-1 px-3 py-1.5 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
                        >
                          <CheckIcon class="w-4 h-4" />
                          {{ vehicle.label }}
                        </span>
                        <span
                          v-if="(vehicleList || []).filter(v => pertanyaan.vehicleTypes[v.id]).length === 0"
                          class="text-sm text-gray-400 italic"
                        >
                          Tidak ada tipe kendaraan dipilih
                        </span>
                      </div>
                    </div>

                    <h1 class="mt-4 text-lg font-bold text-black mb-4">
                      Pertanyaan
                    </h1>

                    <input
                      type="text"
                      :placeholder="pertanyaan.pertanyaan"
                      disabled
                      class="cursor-not-allowed w-full p-2 border border-[#C3C3C3] bg-gray-100 text-gray-700 rounded-md text-sm mb-4"
                    />

                    <label class="block text-base font-bold text-gray-800 mb-2">
                      Jawaban
                    </label>

                    <div class="space-y-3">
                      <div
                        v-for="(jawab, index) in pertanyaan.jawabanList"
                        :key="jawab.id"
                        class="grid grid-cols-2 gap-4"
                      >
                        <div class="relative">
                          <input
                            type="text"
                            :placeholder="jawab.jawaban"
                            disabled
                            class="cursor-not-allowed w-full p-2 border border-[#C3C3C3] bg-gray-100 text-gray-800 rounded-md text-sm"
                          />
                          <PencilIcon
                            class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                          />
                        </div>

                        <div class="relative">
                          <input
                            type="text"
                            :placeholder="jawab.pilihan"
                            disabled
                            class="cursor-not-allowed w-full p-2 border border-[#C3C3C3] bg-gray-100 text-gray-700 rounded-md text-sm"
                          />
                          <ChevronDownIcon
                            class="absolute right-3 top-2.5 w-5 h-5 text-[#b2b2b2]"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Konten tambah pertanyaan -->
            <div
              v-if="tambahPertanyaan"
              class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            >
              <div
                class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-[0_4px_6px_rgba(0,0,0,0.1)] p-6 md:p-8"
              >
                <div
                  class="flex justify-between items-center mb-4 pb-3 border-b border-gray-300"
                >
                  <h2 class="text-lg md:text-xl font-semibold text-gray-900">
                    Tambah Pertanyaan
                  </h2>
                  <button
                    @click="closetambahPertanyaan"
                    class="shrink-0 p-1 hover:bg-gray-100 rounded-md transition"
                  >
                    <XMarkIcon
                      class="w-6 h-6 text-gray-600 hover:text-gray-900"
                    />
                  </button>
                </div>

                <div>
                  <label
                    class="block text-base font-medium text-black mb-2 mt-4"
                    >Tipe kendaraan</label
                  >
                  <div class="grid grid-cols-2 gap-3 md:grid-cols-5">
                    <div
                      v-for="vehicle in (vehicleList || [])"
                      :key="vehicle.id"
                      @click="vehicleTypes[vehicle.id] = !vehicleTypes[vehicle.id]"
                      class="flex items-center gap-2 p-2 border rounded-xl transition cursor-pointer hover:shadow-md active:scale-95"
                      :class="
                        vehicleTypes[vehicle.id]
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-[#a9a9a9] bg-white hover:border-gray-400'
                      "
                    >
                      <div class="relative w-5 h-5 shrink-0">
                        <input
                          type="checkbox"
                          :checked="vehicleTypes[vehicle.id]"
                          :id="`add-${vehicle.id}`"
                          class="w-5 h-5 pointer-events-none rounded-md border-2 appearance-none bg-white border-gray-600 checked:bg-blue-500 checked:border-blue-500"
                          style="
                            appearance: none;
                            -webkit-appearance: none;
                            -moz-appearance: none;
                          "
                          readonly
                        />
                        <CheckIcon
                          v-if="vehicleTypes[vehicle.id]"
                          class="absolute inset-0 m-auto w-4 h-4 text-white pointer-events-none"
                        />
                      </div>
                      <span class="text-sm text-gray-700 select-none">
                        {{ vehicle.label }}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <label
                    class="block text-base font-medium text-black mb-2 mt-4"
                    >Pertanyaan</label
                  >
                  <div class="relative mb-6">
                    <input
                      type="text"
                      v-model="formPertanyaan"
                      placeholder="Masukkan pertanyaan"
                      class="w-full p-2 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
                    />
                    <PencilIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
                    />
                  </div>

                  <label class="block text-base font-medium text-black mb-2"
                    >Kolom Jawaban</label
                  >
                  <div class="space-y-1">
                    <div
                      v-for="(form, index) in formJawabanList"
                      :key="form.id"
                      class="p-2 border border-gray-200 rounded-lg bg-gray-50"
                    >
                      <!-- Header dengan nomor -->
                      <div class="flex justify-between items-center mb-4">
                        <h3 class="font-semibold text-gray-700">
                          Jawaban {{ index + 1 }}
                        </h3>
                        <button
                          v-if="formJawabanList.length > 1"
                          @click="formJawabanList.splice(index, 1)"
                          class="text-red-600 hover:text-red-800 transition"
                        >
                          <TrashIcon class="w-5 h-5" />
                        </button>
                      </div>

                      <!-- Input Jawaban -->
                      <div class="grid grid-cols-2 gap-4">
                        <div class="relative">
                          <input
                            type="text"
                            v-model="form.jawaban"
                            placeholder="Jawaban"
                            class="w-full p-2 border border-[#C3C3C3] bg-white text-gray-700 rounded-md text-sm"
                          />
                          <PencilIcon
                            class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                          />
                        </div>

                        <div class="relative">
                          <select
                            v-model="form.pilihan"
                            class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md text-sm focus:outline-none focus:border-[#A90CF8] appearance-none"
                          >
                            <option value="">Pilih jawaban</option><option value="Normal">Normal</option><option value="Abnormal">Abnormal</option><option value="Warning">Warning</option>
                          </select>
                          <ChevronDownIcon
                            class="absolute right-3 top-2.5 w-5 h-5 text-[#b2b2b2] pointer-events-none"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="flex justify-center mt-6">
                  <button
                    @click="tambahKontainerPertanyaan"
                    class="flex items-center gap-2 px-20 py-2 text-sm border border-blue-300 bg-blue-50 text-blue-700 rounded-xl hover:bg-blue-100 transition font-regular"
                  >
                    <PlusIcon class="w-5 h-5" />
                    Tambah pertanyaan lain
                  </button>
                </div>

                <!-- Button -->
                <div class="flex justify-end gap-3 mt-6">
                  <button
                    @click="simpanPertanyaan"
                    class="px-8 md:px-10 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular"
                  >
                    Simpan
                  </button>
                  <button
                    @click="closetambahPertanyaan"
                    class="px-6 md:px-6 py-2 text-sm md:text-base border border-gray-300 bg-red-600 text-white rounded-xl hover:bg-red-700 transition font-regular"
                  >
                    Batal
                  </button>
                </div>
              </div>
            </div>

            <!-- Konten Edit pertanyaan -->
            <div
              v-if="editPertanyaan"
              class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            >
              <div
                class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-[0_4px_6px_rgba(0,0,0,0.1)] p-6 md:p-8"
              >
                <div
                  class="flex justify-between items-center mb-4 pb-3 border-b border-gray-300"
                >
                  <h2 class="text-lg md:text-xl font-semibold text-gray-900">
                    Edit Pertanyaan
                  </h2>
                  <button
                    @click="closeEditPertanyaan"
                    class="shrink-0 p-1 hover:bg-gray-100 rounded-md transition"
                  >
                    <XMarkIcon
                      class="w-6 h-6 text-gray-600 hover:text-gray-900"
                    />
                  </button>
                </div>

                <div>
                  <label
                    class="block text-base font-medium text-black mb-2 mt-4"
                    >Tipe kendaraan</label
                  >
                  <div class="grid grid-cols-2 gap-3 md:grid-cols-5">
                    <div
                      v-for="vehicle in (vehicleList || [])"
                      :key="vehicle.id"
                      @click="vehicleTypes[vehicle.id] = !vehicleTypes[vehicle.id]"
                      class="flex items-center gap-2 p-2 border rounded-xl transition cursor-pointer hover:shadow-md active:scale-95"
                      :class="
                        vehicleTypes[vehicle.id]
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-[#a9a9a9] bg-white hover:border-gray-400'
                      "
                    >
                      <div class="relative w-5 h-5 shrink-0">
                        <input
                          type="checkbox"
                          :checked="vehicleTypes[vehicle.id]"
                          :id="`edit-${vehicle.id}`"
                          class="w-5 h-5 pointer-events-none rounded-md border-2 appearance-none bg-white border-gray-600 checked:bg-blue-500 checked:border-blue-500"
                          style="
                            appearance: none;
                            -webkit-appearance: none;
                            -moz-appearance: none;
                          "
                          readonly
                        />
                        <CheckIcon
                          v-if="vehicleTypes[vehicle.id]"
                          class="absolute inset-0 m-auto w-4 h-4 text-white pointer-events-none"
                        />
                      </div>
                      <span class="text-sm text-gray-700 select-none">
                        {{ vehicle.label }}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <label
                    class="block text-base font-medium text-black mb-2 mt-4"
                    >Pertanyaan</label
                  >
                  <div class="relative mb-6">
                    <input
                      type="text"
                      v-model="formPertanyaan"
                      placeholder="Masukkan pertanyaan"
                      class="w-full p-2 text-sm border border-[#C3C3C3] bg-white text-gray-700 rounded-sm focus:outline-none focus:border-[#A90CF8]"
                    />
                    <PencilIcon
                      class="absolute right-3 top-2.5 w-5 h-5 text-[#C3C3C3]"
                    />
                  </div>

                  <label class="block text-base font-medium text-black mb-2"
                    >Kolom Jawaban</label
                  >
                  <div class="space-y-1">
                    <div
                      v-for="(form, index) in formJawabanList"
                      :key="form.id"
                      class="p-2 border border-gray-200 rounded-lg bg-gray-50"
                    >
                      <!-- Header dengan nomor -->
                      <div class="flex justify-between items-center mb-4">
                        <h3 class="font-semibold text-gray-700">
                          Jawaban {{ index + 1 }}
                        </h3>
                        <button
                          v-if="formJawabanList.length > 1"
                          @click="formJawabanList.splice(index, 1)"
                          class="text-red-600 hover:text-red-800 transition"
                        >
                          <TrashIcon class="w-5 h-5" />
                        </button>
                      </div>

                      <!-- Input Jawaban -->
                      <div class="grid grid-cols-2 gap-4">
                        <div class="relative">
                          <input
                            type="text"
                            v-model="form.jawaban"
                            placeholder="Jawaban"
                            class="w-full p-2 border border-[#C3C3C3] bg-white text-gray-700 rounded-md text-sm"
                          />
                          <PencilIcon
                            class="absolute right-3 top-2.5 w-4 h-4 text-[#b2b2b2]"
                          />
                        </div>

                        <div class="relative">
                          <select
                            v-model="form.pilihan"
                            class="w-full p-2 pr-10 border border-[#C3C3C3] bg-white text-gray-700 rounded-md text-sm focus:outline-none focus:border-[#A90CF8] appearance-none"
                          >
                            <option value="">Pilih jawaban</option><option value="Normal">Normal</option><option value="Abnormal">Abnormal</option><option value="Warning">Warning</option>
                          </select>
                          <ChevronDownIcon
                            class="absolute right-3 top-2.5 w-5 h-5 text-[#b2b2b2] pointer-events-none"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="flex justify-center mt-6">
                  <button
                    @click="tambahKontainerPertanyaan"
                    class="flex items-center gap-2 px-20 py-2 text-sm border border-blue-300 bg-blue-50 text-blue-700 rounded-xl hover:bg-blue-100 transition font-regular"
                  >
                    <PlusIcon class="w-5 h-5" />
                    Tambah jawaban lain
                  </button>
                </div>

                <!-- Button -->
                <div class="flex justify-end gap-3 mt-6">
                  <button
                    @click="simpanEditPertanyaan"
                    class="px-8 md:px-10 py-2 text-sm md:text-base bg-linear-to-r from-[#A90CF8] to-[#9600E1] text-white rounded-xl hover:opacity-90 transition font-regular"
                  >
                    Simpan
                  </button>
                  <button
                    @click="closeEditPertanyaan"
                    class="px-6 md:px-6 py-2 text-sm md:text-base border border-gray-300 bg-red-600 text-white rounded-xl hover:bg-red-700 transition font-regular"
                  >
                    Batal
                  </button>
                </div>
              </div>
            </div>

            <!-- Modal Konfirmasi Hapus -->
            <div
              v-if="confirmDelete"
              class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            >
              <div
                class="bg-white rounded-lg w-full max-w-md shadow-lg p-6"
              >
                <div class="flex items-center gap-3 mb-4">
                  <div class="shrink-0 w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                    <TrashIcon class="w-6 h-6 text-red-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-900">
                      Konfirmasi Hapus
                    </h3>
                  </div>
                </div>

                <div class="mb-6">
                  <p class="text-gray-700">
                    Apakah Anda yakin ingin menghapus pertanyaan:
                  </p>
                  <p class="font-semibold text-gray-900 mt-2">
                    "{{ pertanyaanToDelete?.pertanyaan }}"
                  </p>
                  <p class="text-sm text-red-600 mt-2">
                    Tindakan ini tidak dapat dibatalkan.
                  </p>
                </div>

                <div class="flex justify-end gap-3">
                  <button
                    @click="batalHapus"
                    class="px-6 py-2 text-sm border border-gray-300 bg-white text-gray-700 rounded-xl hover:bg-gray-50 transition font-regular"
                  >
                    Batal
                  </button>
                  <button
                    @click="konfirmasiHapus"
                    :disabled="loading"
                    class="px-6 py-2 text-sm bg-red-600 text-white rounded-xl hover:bg-red-700 transition font-regular disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ loading ? 'Menghapus...' : 'Iya, Hapus' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
  
  <!-- Vehicle Type Management Modals -->
  <VehicleTypeListModal
    :is-open="vehicleTypeListModal"
    :vehicle-types="allVehicleTypes"
    :loading="vehicleTypeLoading"
    @close="vehicleTypeListModal = false"
    @add="handleAddVehicleType"
    @edit="handleEditVehicleType"
    @delete="handleDeleteVehicleType"
    @refresh="fetchAllVehicleTypes"
  />
  
  <VehicleTypeModal
    :is-open="vehicleTypeModal"
    :edit-mode="vehicleTypeEditMode"
    :vehicle-type="currentVehicleType"
    :loading="vehicleTypeLoading"
    @close="vehicleTypeModal = false"
    @submit="handleVehicleTypeSubmit"
  />
</template>
