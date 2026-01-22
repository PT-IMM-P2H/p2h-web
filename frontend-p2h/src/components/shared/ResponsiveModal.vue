<script setup>
import { defineProps, defineEmits, computed } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'full'].includes(value)
  },
  showClose: {
    type: Boolean,
    default: true
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const sizeClasses = computed(() => {
  const sizes = {
    small: 'max-w-sm sm:max-w-md',
    medium: 'max-w-md sm:max-w-lg md:max-w-xl',
    large: 'max-w-lg sm:max-w-xl md:max-w-2xl lg:max-w-4xl',
    full: 'max-w-full'
  }
  return sizes[props.size]
})

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    emit('close')
  }
}

const handleClose = () => {
  emit('close')
}
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-2 sm:p-4"
        @click="handleOverlayClick"
      >
        <Transition
          enter-active-class="transition-all duration-200"
          enter-from-class="opacity-0 scale-95 translate-y-4"
          enter-to-class="opacity-100 scale-100 translate-y-0"
          leave-active-class="transition-all duration-200"
          leave-from-class="opacity-100 scale-100 translate-y-0"
          leave-to-class="opacity-0 scale-95 translate-y-4"
        >
          <div
            v-if="isOpen"
            :class="[
              'bg-white rounded-lg shadow-xl w-full max-h-[90vh] sm:max-h-[85vh] flex flex-col overflow-hidden',
              sizeClasses
            ]"
            @click.stop
          >
            <!-- Header -->
            <div class="flex items-center justify-between px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200 shrink-0">
              <h3 class="text-base sm:text-lg md:text-xl font-semibold text-gray-800 truncate pr-2">
                {{ title }}
              </h3>
              <button
                v-if="showClose"
                @click="handleClose"
                class="p-1.5 sm:p-2 hover:bg-gray-100 rounded-lg transition-colors shrink-0"
                aria-label="Tutup modal"
              >
                <XMarkIcon class="w-5 h-5 sm:w-6 sm:h-6 text-gray-500" />
              </button>
            </div>

            <!-- Body -->
            <div class="flex-1 overflow-y-auto px-4 sm:px-6 py-3 sm:py-4">
              <slot></slot>
            </div>

            <!-- Footer (optional) -->
            <div v-if="$slots.footer" class="px-4 sm:px-6 py-3 sm:py-4 border-t border-gray-200 shrink-0">
              <slot name="footer"></slot>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>
