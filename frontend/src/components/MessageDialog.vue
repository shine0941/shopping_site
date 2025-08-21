<template>
  <v-dialog v-model="localActive" width="40vw" min-height="20vh">
    <v-card style="overflow: hidden">
      <v-row>
        <v-col style="align-content: center; text-align: center">
          {{ props.message }}
        </v-col>
      </v-row>
      <v-row>
        <v-col style="text-align: center">
          <v-btn @click="localActive = !localActive" color="primary">Close</v-btn>
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>
<script setup>
import { ref, watch } from 'vue'
import router from '@/router'
const props = defineProps({
  isActive: {
    type: Boolean,
    default: false,
  },
  message: {
    type: String,
    default: 'Message dialog default message',
  },
})

const localActive = ref(props.isActive)
const emit = defineEmits(['update:isActive'])
watch(
  () => props.isActive,
  (val) => {
    localActive.value = val
  },
)
watch(localActive, (val) => {
  emit('update:isActive', val)
})
</script>
