<template>
  <v-menu open-on-hover>
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props"> <v-icon size="x-large">mdi-account</v-icon>{{ user.username }} </v-btn>
    </template>
    <v-list>
      <v-list-item v-for="(item, index) in items" :key="index" :value="index" :to="item.to">
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
  <!-- <v-btn color="primary">
    Parent activator

    <v-menu activator="parent">
      <v-list>
        <v-list-item v-for="(item, index) in items" :key="index" :value="index">
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-btn> -->
</template>
<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
const user = useUserStore()
const items = ref([{ title: 'Order History', to: '/orderhistory/' }])
</script>
