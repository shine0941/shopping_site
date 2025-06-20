<template>
  <v-app>
    <div style="display: flex">
      <div>
        <div>
          <AdminAppBar @switch-drawer="drawer = !drawer"></AdminAppBar>
        </div>
      </div>
      <div>
        <div>
          <AdminDrawer v-model:drawer="drawer"></AdminDrawer>
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
import AdminAppBar from '@/components/AdminAppBar.vue'
import AdminDrawer from '@/components/AdminDrawer.vue'

const drawer = ref(true)
const user = useUserStore()

const mountedLog = () => {
  console.log('mountedLog onMounted')
  user.init()
}
onMounted(mountedLog)
</script>
