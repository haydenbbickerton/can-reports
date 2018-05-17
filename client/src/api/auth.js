import config from 'config'
import request from '@/utils/request'

export function login(username, password) {
  return request({
    url: config.api.authUrl,
    method: 'post',
    data: {
      username,
      password
    }
  })
}