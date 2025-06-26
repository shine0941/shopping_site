<template>
  <v-navigation-drawer color="" :model-value="drawer" @update:modelValue="emitDrawer">
    <v-list nav>
      <v-list-item title="All products" to="/" link elevation="0" hover></v-list-item>
      <v-list-item
        v-for="d in drawer_list"
        :title="d.name"
        :to="'/' + d.id"
        link
        elevation="0"
        hover
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
const props = defineProps({
  drawer: Boolean,
})
const emit = defineEmits(['update:drawer'])
const emitDrawer = (val) => {
  emit('update:drawer', val)
}
const drawer_list = ref([])
const initCategory = async () => {
  const res = await api.fetchProductCategories()
  drawer_list.value = res.data.map((category) => {
    return {
      ...category,
    }
  })
}
onMounted(initCategory)
</script>
