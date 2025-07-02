<template>
  <v-container style="max-width: 50vw; width: 30vw">
    <v-form @submit.prevent="submit_login">
      <h3>Login</h3>
      <v-text-field
        v-model="email"
        label="帳號"
        type="email"
        clearable
        hint="Enter your password to access this website"
        :rules="[rules.required, rules.email]"
      />
      <v-text-field
        v-model="password"
        label="密碼"
        :type="show1 ? 'text' : 'password'"
        clearable
        hint=""
        :rules="[rules.required]"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append="show1 = !show1"
      />
      <v-row>
        <v-spacer></v-spacer>
        <v-col style="text-align: right"
          ><v-btn type="submit" color="secondary" :disabled="!isLoginFormValid">Login</v-btn></v-col
        >
      </v-row>
    </v-form>
  </v-container>
</template>
<script setup>
import { ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const user = useUserStore()

const email = ref('admin@example.com')
// const email = ref('merchant@merchant.com')
const password = ref('Passw0rd!')
const show1 = ref(false)

const submit_login = async () => {
  try {
    await user.admin_login(email.value, password.value)
    router.push('/admin/')
  } catch (err) {
    alert('登入失敗', err)
  }
}
const rules = {
  required: (value) => !!value || 'Required.',
  email: (value) => {
    const pattern =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'Invalid e-mail.'
  },
  passwordMatch: () => password_confirm.value === password.value || 'Not match',
}
const isLoginFormValid = computed(() => {
  return (
    rules.required(email.value) === true &&
    rules.email(email.value) === true &&
    rules.required(password.value) === true
  )
})
</script>
