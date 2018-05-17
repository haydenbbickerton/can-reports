import Vue from 'vue'
import config from 'config'



import App from './App'
import router from './router'
import store from './store'
import { sync } from 'vuex-router-sync'
import './plugins'

Vue.config.productionTip = false
sync(store, router)

new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
