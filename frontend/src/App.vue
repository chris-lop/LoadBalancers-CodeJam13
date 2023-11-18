<template>
  <div>
    <router-view />
    <Menubar class="fixed top-0 left-0 right-0" :model="items">
      <template #item="{ item }">
        <router-link :to="item.to" class="p-3">
          <i :class="item.icon"></i>
          <span class="pl-2">{{ item.label }}</span>
        </router-link>
      </template>
    </Menubar>
  </div>
</template>

<script>
  export default {
    name: "App",
    data() {
      return {
        items: [
          {
            label: "Home",
            icon: "pi pi-fw pi-home",
            to: "/"
          },
          {
            label: "Login",
            icon: "pi pi-fw pi-sign-in",
            to: "/login"
          }
        ],
        checked: false
      }
    },
    created() {
      
    },
    methods: {
      
    },
    computed: {
      capitalizedRouteName() {
        const routeName = this.$route.name
        return routeName ? routeName.charAt(0).toUpperCase() + routeName.slice(1) : ''
      }
    }
  }
</script>

<style>

</style>


