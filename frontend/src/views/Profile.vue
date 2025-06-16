<template>
  <v-container style="max-width: 100vw">
    <h2>user profile</h2>
    <v-row style="width: 50vw">
      <v-col>
        <v-text-field v-model="username" label="username" prepend-icon="mdi-account"></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col style="text-align: right">
        <v-btn color="primary" @click="submit">update</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { useUserStore } from '@/stores/user'
import { ref } from 'vue'
const user = useUserStore()
const username = ref(user.username)
const submit = () => {
  user.updateUsername(username.value)
}
</script>
