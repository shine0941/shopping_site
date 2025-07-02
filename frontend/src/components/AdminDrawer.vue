<template>
  <v-navigation-drawer color="" v-model="props.drawer">
    <v-list nav>
      <v-list-item
        v-for="d in drawer_list"
        :title="d.title"
        :to="d.to"
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
const drawer_list = ref([
  { title: 'Product List', to: '/admin/products' },
  { title: 'Order List', to: '/admin/orders' },
  { title: 'Sales Report', to: '/admin/sales' },
  { title: 'Customer Service', to: '/admin/chats' },
])
</script>
