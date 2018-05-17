import config from 'config'
import request from '@/utils/request'

export function getPucMessagesReport() {
  return request.get('/reports/puc_messages')
}

export function postGpsMessage(data) {
  return request({
    url: '/messages/gps/',
    method: 'post',
    data
  })
}

