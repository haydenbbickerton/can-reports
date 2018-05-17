import { login } from '@/api/auth'

const user = {
  namespaced: true,
  state: {
    token: null,
    username: ''
  },

  getters: {
    authenticated: (state, getters) => {
      return !!state.token
    }
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_USERNAME: (state, username) => {
      state.username = username
    }
  },

  actions: {

    Login({ commit }, userInfo) {
      const username = userInfo.username.trim()
      return new Promise((resolve, reject) => {
        login(username, userInfo.password).then(response => {
          const data = response.data
          commit('SET_TOKEN', data.token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    Logout({ commit, state }) {
      return new Promise((resolve, reject) => {
        commit('SET_TOKEN', null)
        resolve()
      })
    }
  }
}

export default user
