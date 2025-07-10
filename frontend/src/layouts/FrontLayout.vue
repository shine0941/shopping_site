<template>
  <v-app>
    <div style="display: flex">
      <!-- v-if="$deviceType == 'desktop'" -->
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
    <div style="position: fixed; bottom: 3vh; right: 3vw">
      <!-- <ChatDialog></ChatDialog> -->
    </div>
    <!-- <div v-else class="min-h-screen bg-gray-100 p-4">
      <MobileAppBar></MobileAppBar>
      <div style="margin-top: 64px"><RouterView /></div>
      <MobileFooter></MobileFooter>
    </div> -->
  </v-app>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AppBar from '@/components/AppBar.vue'
import AppDrawer from '@/components/AppDrawer.vue'
import MobileAppBar from '@/components/MobileAppBar.vue'
import MobileFooter from '@/components/MobileFooter.vue'
import ChatDialog from '@/components/ChatDialog.vue'

const drawer = ref(true)
const user = useUserStore()

const mountedLog = () => {
  console.log('FrontLayout onMounted')
  user.init()
}
onMounted(mountedLog)
</script>
