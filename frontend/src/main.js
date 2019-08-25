import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Routes from './router'
import Notifications from 'vue-notification'
import VueChatScroll from 'vue-chat-scroll'
import store from './store'

import VueMoment from 'vue-moment'
import moment from 'moment-timezone'

import VueNativeSock from 'vue-native-websocket'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import {Socket} from './socket'
import init_axios from "./axios";
import {API_URL, LOCAL_URL, WS_URL} from "./vars";


Vue.use(BootstrapVue);
Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(Notifications);
Vue.use(VueChatScroll);
Vue.use(VueMoment, {moment,});
Vue.use(VueNativeSock, WS_URL, {
  format: 'json',
  connectManually: true
});

const router = new VueRouter({
  routes: Routes,
  mode: 'history'
});

router.beforeEach((to, from, next) => {
  if (!store.state.initialized){
    store.dispatch('update_user').then(() => {
      next()
    })
  }
  else {
    next();
  }
});


let myAxios = init_axios(API_URL, null, (err) => {
  if (err.response.status === 401) {
    store.commit('logout');
    if (router.currentRoute.matched.length > 0 && router.currentRoute.matched[0].meta.auth) {
      router.push('/login');
      router.go(0);
    }
  }
  throw err;
});



let vue = new Vue({
  router: router,
  store,
  render: h => h(App),
  data: {
    API_URL: API_URL,
    LOCAL_URL: LOCAL_URL,
    axios: myAxios
  }
}).$mount('#app');
vue.$options.sockets.onmessage = Socket.socketHandler;
