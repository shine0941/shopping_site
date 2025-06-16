<template>
  <v-menu open-on-hover>
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" :prepend-icon="btn_icon">{{ btn_text }}</v-btn>
    </template>
    <v-list>
      <v-list-item
        v-for="(item, index) in items"
        :key="index"
        :value="index"
        :prepend-icon="item.icon"
        @click="changeOrdering(item, item)"
      >
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script setup>
import { ref, watch } from 'vue'
// const props = defineProps({
//   ordering: {
//     type: String,
//     default: '-created_at',
//   },
// })
const emit = defineEmits(['changeOrdering'])
const btn_icon = ref('mdi-sort')
const btn_text = ref('')
const items = ref([
  {
    title: 'Newest',
    ordering: '-created_at',
    icon: 'mdi-sort-clock-ascending-outline', // 最新在前
  },
  {
    title: 'Oldest',
    ordering: 'created_at',
    icon: 'mdi-sort-clock-descending-outline', // 最舊在前
  },
  {
    title: 'Price ↓',
    ordering: '-price',
    icon: 'mdi-sort-ascending', // 價格高到低
  },
  {
    title: 'Price ↑',
    ordering: 'price',
    icon: 'mdi-sort-descending', // 價格低到高
  },
])
const changeOrdering = (item) => {
  console.log('changeOrdering', item.ordering)
  btn_icon.value = item.icon
  btn_text.value = item.title
  emit('changeOrdering', item.ordering)
}
</script>
