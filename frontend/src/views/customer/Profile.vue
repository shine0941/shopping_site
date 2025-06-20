<template>
  <v-container style="max-width: 100vw; width: 50vw">
    <h2>User Profile</h2>
    <br />
    <v-row>
      <v-col>
        <v-text-field
          v-model="email"
          label="email"
          prepend-icon="mdi-email-outline"
          :readonly="true"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field v-model="username" label="Username" prepend-icon="mdi-account"></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          v-model="bday"
          label="Birthday"
          prepend-icon="mdi-cake-variant"
          type="date"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          v-model="memberlevel"
          label="Member Level"
          prepend-icon="mdi-wallet-membership"
          :readonly="true"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col style="text-align: right">
        <v-btn color="primary" @click="submit" :loading="loading">Update</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { useUserStore } from '@/stores/user'
import { onMounted, ref } from 'vue'
const user = useUserStore()
const username = ref(user.username)
const email = ref('')
const bday = ref('')
const memberlevel = ref('')
const loading = ref(false)
const submit = async () => {
  loading.value = true
  const params = {}
  if (username && username != user.username) {
    params['full_name'] = username.value
  }
  if (bday) {
    params['birthday'] = bday.value
  }

  await user.updateUsername(params)
  loading.value = false
}
const init = async () => {
  const res = await user.fetchUserInfo()
  console.log(res)
  email.value = res.user.email
  bday.value = res.birthday
  memberlevel.value = res.membership_level
}
onMounted(init)
</script>
