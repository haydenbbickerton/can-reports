import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import router from '@/router'
import config from 'config'

// create an axios instance
const service = axios.create({
  baseURL: config.api.baseUrl,
  timeout: 5000
})

// request interceptor
service.interceptors.request.use(config => {
  if (store.getters.token) {
    // Add the auth token to every request
    config.headers.Authorization = `JWT ${store.getters.token}`
  }
  return config
}, error => {
  console.log(error)
  Promise.reject(error)
})

// response interceptor
service.interceptors.response.use(
  response => response,
  error => {
    let message = error.message

    if (error.response.status == 401) {
      console.log('Auth token invalid')
      message = 'Your session has expired, please log back in.'
      router.push({name: 'Login'})
    }

    console.log('err' + error)
    // UI popup with the error message
    Message({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })

    return Promise.reject(error)
  })

export default service
