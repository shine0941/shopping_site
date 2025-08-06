<template>
  <v-dialog v-model="localActive" width="40vw" min-height="20vh">
    <v-card style="overflow: hidden">
      <v-row>
        <v-col style="align-content: center; text-align: center">
          Please sign in to add products to your cart.
        </v-col>
      </v-row>
      <v-row>
        <v-col style="text-align: center">
          <v-btn @click="router.push('/login')" color="primary">Go to Login</v-btn>
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
