import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Routes from './router'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);
Vue.config.productionTip = false;
Vue.use(VueRouter);

const router = new VueRouter({
  routes: Routes,
  mode: 'history'
});

const authData = localStorage.getItem('auth');

new Vue({
  render: h => h(App),
  router: router,
  data: {
    auth: authData ? JSON.parse(authData) : {}
  }
}).$mount('#app');
