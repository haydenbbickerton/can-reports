import config from 'config'

const socket = {
  namespaced: true,
  state: {
    data: {}
  },

  mutations: {
    SET_DATA: (state, data) => {
      state.data = data
    },
  },

  actions: {
    listenToSocket({ commit, dispatch }) {
      const ws = new WebSocket(config.socketUrl)
      ws.onmessage = e => dispatch('newSocketMessage', e.data)
      commit('SET_DATA', {}) // Hack since the persistence storage thing is messing with stuff that isn't specified
    },
    newSocketMessage({ commit, state }, data) {
      try {
        data = JSON.parse(data)
      } catch (e) {
        console.log(e)
        console.error('Could not parse socket message as JSON')
      }
      commit('SET_DATA', data)
    }
  }
}

export default socket
