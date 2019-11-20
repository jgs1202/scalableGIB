import Vue from 'vue'
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/ja'
import 'element-ui/lib/theme-chalk/index.css'
import home from './home.vue'

Vue.use(ElementUI, {locale})

new Vue({
  el: '#app',
  render: h => h(home)
})
