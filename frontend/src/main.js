import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Routes from './router'
import Notifications from 'vue-notification'
import VueChatScroll from 'vue-chat-scroll'
import Moment from 'moment-timezone'

import VueNativeSock from 'vue-native-websocket'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import {Socket} from './socket'
import init_axios from "./axios";


const API_URL = "https://matchaaa.tk/api";
const WS_URL = "wss://matchaaa.tk/ws";
const LOCAL_URL = "https://matchaaa.tk";


Vue.use(BootstrapVue);
Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(Notifications);
Vue.use(VueChatScroll);
Vue.use(Moment);

Vue.use(VueNativeSock, WS_URL, { format: 'json' });

const router = new VueRouter({
  routes: Routes,
  mode: 'history'
});

const userId = localStorage.getItem('user_id');
const userData = localStorage.getItem('user');

let vue = new Vue({
  router: router,
  data: {
    user_id: userId ? userId : null,
    user: userData ? JSON.parse(userData) : {},
    API_URL: API_URL,
    LOCAL_URL: LOCAL_URL,
    axios: init_axios(API_URL, null, (err) => {
      if (err.response.status === 401) {
        localStorage.removeItem('user');
        localStorage.removeItem('user_id');
        if (router.currentRoute.matched.length > 0 && router.currentRoute.matched[0].meta.auth) {
          router.push('/login');
          router.go(0);
        }
      }
      throw err;
    })
  },
  render: h => h(App)
}).$mount('#app');
vue.$options.sockets.onmessage = Socket.socketHandler;
