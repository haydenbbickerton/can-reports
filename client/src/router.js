import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

Vue.use(Router)

/* Layout */
import Layout from '@/views/layout/Layout'

export const constantRouterMap = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/realtime',
    name: 'Layout',
    hidden: true,
    children: [
    {
        path: '/realtime',
        name: 'Realtime',
        component: () => import('@/views/Realtime'),
    },
    {
        path: '/summary',
        name: 'Summary',
        component: () => import('@/views/Summary'),
    }
    ]
  },
  { path: '*', redirect: '/realtime', hidden: true }
]

const router = new Router({
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

router.beforeEach((to, from, next) => {
  if (to.name == 'Login') {
    store.dispatch('user/Logout')
    next()
  }

  if (!store.getters['user/authenticated'] && to.name != 'Login') {
    next({ path: 'Login' })
  } else {
    next()
  }
})

export default router
