import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Routes from './router'
import {Auth} from './auth'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);
Vue.config.productionTip = false;
Vue.use(VueRouter);

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

const authData = localStorage.getItem('auth');

new Vue({
  render: h => h(App),
  router: router,
  data: {
    API_URL: "http://localhost:5000",
    Auth: Auth,
    auth: authData ? JSON.parse(authData) : {}
  }
}).$mount('#app');
