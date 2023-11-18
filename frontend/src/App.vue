<template> 
    <div>
      <router-view />
      <Menubar class="fixed top-0 left-0 right-0" :model="items">
        <template #item="{item}">
          <router-link :to="item.to" class="p-3">
            <i :class="item.icon"></i>
            <span class="pl-2">{{item.label}}</span>
          </router-link>
        </template>
        <template #end>
        <div class="flex align-items-center gap-2">
          <InputSwitch v-model="checked" class="absolute right-0 top-0" />
        </div>
        </template>
      </Menubar>
      <Card class="fixed top-10 left-0 right-0 h-20 mt-[0.35%]">
        <template #title>
          <div class="pl-3">
            {{capitalizedRouteName}}
          </div>
        </template>
      </Card>
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


