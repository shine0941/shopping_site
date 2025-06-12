<template>
  <div
    v-if="display"
    style="color: white; width: fit-content; padding: 5px"
    :style="{ 'background-color': bgcolor }"
  >
    <v-icon>{{ icon }}</v-icon> {{ text }}
  </div>
</template>
<script setup>
import { mergeProps, onMounted, ref } from 'vue'
const props = defineProps({
  product_info: Object,
})
const display = ref(false)
const icon = ref('')
const text = ref('')
const bgcolor = ref('')
const initLabel = () => {
  if (props.product_info.inventory <= 10) {
    display.value = true
    icon.value = 'mdi-alert-decagram'
    text.value = 'Running Low'
    bgcolor.value = 'orange'
  } else if (props.product_info.sold_count > 10) {
    display.value = true
    icon.value = 'mdi-fire'
    text.value = 'Hot Selling'
    bgcolor.value = 'red'
  } else if (props.product_info.discount_percent < 100) {
    display.value = true
    icon.value = 'mdi-sale'
    text.value = 'Special Price'
    bgcolor.value = 'orangered'
  }
}
onMounted(initLabel)
</script>
