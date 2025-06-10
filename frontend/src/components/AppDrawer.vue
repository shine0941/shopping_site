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

      <!-- <v-list-item :title="$vuetify.display.mobile" link></v-list-item> -->
    </v-list>
  </v-navigation-drawer>
</template>
<script setup>
import { ref, watch, onMounted } from 'vue'
const props = defineProps({
  drawer: Boolean,
})

const drawer_list = ref([
  { title: '相機', to: '/1' },
  { title: '電腦', to: '/2' },
  { title: '手機', to: '/3' },
  { title: '平板', to: '/4' },
])
</script>
