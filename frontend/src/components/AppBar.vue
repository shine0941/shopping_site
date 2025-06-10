<template>
  <v-app-bar :elevation="2" color="primary">
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click.stop="emit('switch-drawer')"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title>
      <div @click="goHome" style="cursor: pointer; width: fit-content">Shopping.com</div>
    </v-app-bar-title>
    <template v-slot:append>
      <!-- <v-btn v-if="user.token">
        <template v-slot:prepend>
          <v-icon size="x-large">mdi-account</v-icon>
        </template>
        {{ user.username }}
      </v-btn> -->
      <UserDialog></UserDialog>
      <v-divider vertical inset></v-divider>
      <CartDIalog></CartDIalog>
      <v-divider vertical inset></v-divider>
      <v-btn v-if="user.token" icon="mdi-logout" @click="user.logout"></v-btn>
      <v-btn v-else icon="mdi-login" to="/login/"></v-btn>

      <!-- <v-btn icon="mdi-dots-vertical"></v-btn> -->
    </template>
  </v-app-bar>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import CartDIalog from './CartDIalog.vue'
import UserDialog from './UserDialog.vue'

const emit = defineEmits(['switch-drawer'])
const user = useUserStore()
const router = useRouter()
const goHome = (product) => {
  console.log('goDetail', product)
  router.push(`/`)
}
</script>
