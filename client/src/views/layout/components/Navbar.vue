<template>
  <el-menu class="navbar" mode="horizontal" :router="true" :default-active="$route.path">

    <el-menu-item v-for="route in routes" v-if="!route.hidden"
        :index="route.path"
        :key="route.name"
        :route="route">
        {{ route.name }}
    </el-menu-item>

    <el-menu-item class="logout-btn" style="float:right;" @click="logout" index="logout">
        Logout
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  computed: {
    routes() {
      return this.$router.options.routes.find(route => route.name == 'Layout').children
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('user/Logout').then(() => {
        location.reload()
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.navbar {
  height: 50px;
  line-height: 50px;
  border-radius: 0px !important;
  .screenfull {
    position: absolute;
    right: 90px;
    top: 16px;
    color: red;
  }
}
</style>

