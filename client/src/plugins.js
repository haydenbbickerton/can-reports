import Vue from 'vue'
import config from 'config'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en'
import * as VueGoogleMaps from 'vue2-google-maps'

Vue.use(ElementUI, { locale })
Vue.use(VueGoogleMaps, {
  load: {
    key: config.googleMapsApiKey,
    libraries: 'places',
    installComponents: true,
  }
})
