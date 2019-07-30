import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Routes from './router'
import Notifications from 'vue-notification'
import VueChatScroll from 'vue-chat-scroll'
import Moment from 'moment-timezone'
// import {Auth} from './auth'
import VueNativeSock from 'vue-native-websocket'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import {Socket} from './socket'


Vue.use(BootstrapVue);
Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(Notifications);
Vue.use(VueChatScroll);
Vue.use(Moment);
Vue.use(VueNativeSock, 'wss://matchaaa.tk/ws', { format: 'json' });

const router = new VueRouter({
  routes: Routes,
  mode: 'history'
});

// const ifAuthenticated = (to, from, next) => {
//   if (document.cookie)
//   {
//     next();
//     return
//   }
//   next('/login')
// };
//
// const ifNotAuthenticated = (to, from, next) => {
//   if (!document.cookie)
//   {
//     next();
//     return
//   }
//   next('/')
// };
//
// const isAuth = this.session;

const userId = localStorage.getItem('user_id');
const userData = localStorage.getItem('user');

let vue = new Vue({
  router: router,
  data: {
    user_id: userId ? userId : null,
    user: userData ? JSON.parse(userData) : {},
    // API_URL: "http://ivart:5000",
    // API_URL: "https://api.matchaaa.tk",
    API_URL: "https://matchaaa.tk/api", // TODO: keep this one
    // API_URL: " http://localhost:5000"
    // LOCAL_URL: "https://matchaaa.tk"

    // Auth: Auth,
  },
  render: h => h(App)
}).$mount('#app');
vue.$options.sockets.onmessage = Socket.socketHandler;
