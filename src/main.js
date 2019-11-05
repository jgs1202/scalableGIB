import Vue from 'vue'
import {
    Row,
    Col,
    Alert,
    Select,
    Radio,
    Input,
    Option,
    Dropdown,
    DropdownMenu,
    DropdownItem,
    Button,
    Form,
    FormItem,
    Slider,
    Container,
    Aside,
    Header,
    Main,
    Footer
} from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(Row)
Vue.use(Col)
Vue.use(Alert)
Vue.use(Select)
Vue.use(Input)
Vue.use(Radio)
Vue.use(Option)
Vue.use(Dropdown)
Vue.use(DropdownMenu)
Vue.use(DropdownItem)
Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Slider)
Vue.use(Container)
Vue.use(Aside)
Vue.use(Header)
Vue.use(Main)
Vue.use(Footer)
import home from './home.vue'

new Vue({
  el: '#app',
  render: h => h(home)
})
