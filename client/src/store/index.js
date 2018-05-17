import Vue from 'vue'
import Vuex from 'vuex'
import VuejsStorage from 'vuejs-storage'
import user from './modules/user'
import socket from './modules/socket'
import getters from './getters'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    user,
    socket
  },
  plugins: [
    VuejsStorage({
      keys: ['user', 'socket'],
      namespace: 'canreports'
    })
  ],
  getters
})

export default store
