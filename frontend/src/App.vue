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
import { ref, watch, onMounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AppBar from './components/AppBar.vue'
import AppDrawer from './components/AppDrawer.vue'

const drawer = ref(true)
const user = useUserStore()

const mountedLog = () => {
  console.log('mountedLog onMounted')
  user.init()
}
onMounted(mountedLog)
</script>
<style>
main {
  /* position: fixed; */
  /* top: 64px; */
  /* left: calc(100% - 64px); */
}
</style>
<!-- <style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style> -->
