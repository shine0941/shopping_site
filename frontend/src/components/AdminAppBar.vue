<template>
  <v-app-bar :elevation="2" color="secondary">
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click.stop="emit('switch-drawer')"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title>
      <div @click="goHome" style="cursor: pointer; width: fit-content">Shopping.com Backend</div>
    </v-app-bar-title>
    <template v-slot:append>
      <v-divider vertical inset></v-divider>
      <v-btn> <v-icon>mdi-account</v-icon>{{ user.username }} </v-btn>
      <v-divider vertical inset></v-divider>
      <v-tooltip v-if="user.token" text="Logout" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon="mdi-logout" @click="user.admin_logout"></v-btn>
        </template>
      </v-tooltip>
      <v-tooltip v-else text="Login" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon="mdi-login" to="/admin/login/"></v-btn>
        </template>
      </v-tooltip>

      <!-- <v-btn icon="mdi-dots-vertical"></v-btn> -->
    </template>
  </v-app-bar>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
// import CartDIalog from './CartDIalog.vue'
// import UserDialog from './UserDialog.vue'

const emit = defineEmits(['switch-drawer'])
const user = useUserStore()
const router = useRouter()
const goHome = (product) => {
  console.log('goDetail', product)
  router.push(`/admin/`)
}
</script>
