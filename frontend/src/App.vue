<template>
  <v-app>
    <div style="display: flex">
      <div>
        <div>
          <v-app-bar :elevation="2" color="primary">
            <template v-slot:prepend>
              <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            </template>

            <v-app-bar-title>
              <div @click="goHome" style="cursor: pointer; width: fit-content">Application Bar</div>
            </v-app-bar-title>
            <template v-slot:append>
              <v-btn v-if="user.token">
                <template v-slot:prepend>
                  <v-icon size="x-large">mdi-account</v-icon>
                </template>
                {{ user.username }}
              </v-btn>
              <v-divider vertical inset></v-divider>
              <CartDIalog></CartDIalog>
              <v-divider vertical inset></v-divider>
              <v-btn v-if="user.token" icon="mdi-logout" @click="user.logout"></v-btn>
              <v-btn v-else icon="mdi-login" to="/login/"></v-btn>

              <!-- <v-btn icon="mdi-dots-vertical"></v-btn> -->
            </template>
          </v-app-bar>
        </div>
      </div>
      <div>
        <div>
          <v-navigation-drawer color="" v-model="drawer">
            <v-list nav>
              <v-list-item
                v-for="d in drawer_list"
                :title="d.title"
                link
                elevation="0"
                hover
              ></v-list-item>

              <!-- <v-list-item :title="$vuetify.display.mobile" link></v-list-item> -->
            </v-list>
          </v-navigation-drawer>
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
import { cartStore } from './stores/cart'
// import HelloWorld from './components/HelloWorld.vue'
import CartDIalog from './views/CartDIalog.vue'
const router = useRouter()
const drawer = ref(true)
const user = useUserStore()
const cart = cartStore()

const drawer_list = ref([
  { title: '相機' },
  { title: '電腦' },
  { title: '手機' },
  { title: '平板' },
])

const goHome = (product) => {
  console.log('goDetail', product)
  router.push(`/`)
}
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
