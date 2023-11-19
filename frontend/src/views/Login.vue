<template>
  <Toast />
  <Container class="flex flex-col">
    <div class="flex items-center justify-center flex-grow mt-28">
      <Card class="w-full max-w-xs">
        <template #title>
          <div class="text-center">
            Trucker Login
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <InputText v-model="username" placeholder="Trucker ID" class="w-full mb-4" />
            <Button @click="authenticateTrucker" label="Login" class="w-full" />
          </div>
        </template>
      </Card>
    </div>
  </Container>
</template>

<script>
import Container from "@/components/Container.vue";
import axios from 'axios'
const baseUrl = import.meta.env.VITE_API_SERVER_URL
export default {
  name: "Login",
  components: {
    Container,
  },
  data() {
    return {
      username: '',
    };
  },
  methods: {
    async authenticateTrucker() {
      try {
        await axios.get(`${baseUrl}/metrics/${Number(this.username)}`)
        this.$router.push({ name: 'TruckerMetrics', params: { username: this.username } })
      } catch (error) {
        
        if (error.response && error.response.status === 404) {
          console.log(error.response)
          this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Trucker not found', life: 3000 })
        }
        else {
          console.log(error)
          throw error
        }
      }
    }
  },
};
</script>