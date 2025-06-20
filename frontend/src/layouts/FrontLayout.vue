<template>
  <v-app>
    <div style="display: flex">
      <div>
        <div>
          <AppBar @switch-drawer="drawer = !drawer"></AppBar>
        </div>
      </div>
      <div>
        <div>
          <AppDrawer v-model:drawer="drawer"></AppDrawer>
        </div>
        <div>
          <v-main color="">
            <RouterView />
          </v-main>
        </div>
      </div>
    </div>
  </v-app>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AppBar from '@/components/AppBar.vue'
import AppDrawer from '@/components/AppDrawer.vue'

const drawer = ref(true)
const user = useUserStore()

const mountedLog = () => {
  console.log('mountedLog onMounted')
  user.init()
}
onMounted(mountedLog)
</script>
