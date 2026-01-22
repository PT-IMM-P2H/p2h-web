<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  value: {
    type: [String, Number],
    default: ''
  },
  icon: {
    type: Object,
    default: null
  },
  iconColor: {
    type: String,
    default: 'text-gray-600'
  },
  valueColor: {
    type: String,
    default: 'text-gray-800'
  },
  clickable: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = () => {
  if (props.clickable) {
    emit('click')
  }
}
</script>

<template>
  <div
    :class="[
      'bg-white rounded-lg shadow-md p-2 sm:p-3 md:p-4 flex items-start gap-2 sm:gap-3 min-h-20',
      clickable ? 'cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200' : ''
    ]"
    @click="handleClick"
  >
    <!-- Icon -->
    <component
      v-if="icon"
      :is="icon"
      :class="['w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 shrink-0 mt-0.5', iconColor]"
    />
    
    <!-- Content -->
    <div class="flex flex-col flex-1 min-w-0">
      <p class="text-xs sm:text-sm font-regular text-gray-500 truncate">
        {{ title }}
      </p>
      <h3 :class="['text-base sm:text-lg md:text-xl lg:text-2xl font-bold mt-0.5 sm:mt-1', valueColor]">
        {{ value }}
      </h3>
    </div>
  </div>
</template>
