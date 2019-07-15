<template>
  <div id="app">
<!--    <AppHeader v-bind:session="session" v-on:del_session="deleteSession"/>-->
    <AppHeader/>
    <router-view></router-view><!-- Main routing enter point -->
      <notifications group="foo"/>
    <Footer/>
  </div>
</template>

<script>

import Header from "./components/Header";
import Footer from "./components/Footer";
// import './assets/_custom.scss'

export default {
  name: 'app',
  components: {
    AppHeader: Header,
    Footer
  },
    data() {
      return {
        // session: {
        //   'user_id': null,
        //   'context': {}
        // }
      }
    },

    methods: {
      // deleteSession() {
      //   this.session.user_id = null;
      //   this.session.context = {}
      // }
    },
      // created() {
      //   axios.get(this.$root.API_URL + '/auth/whoami', {withCredentials: true})
      //       .then(response => this.session = response.data)
      //
      //       // .then(response => console.log(response.data))
      //       .catch(error => console.log(error));
      // }
}
</script>

<style lang="scss">
  @import 'assets/_custom.scss';
  @import '~bootstrap/scss/bootstrap.scss';
  @import '~bootstrap-vue/src/index.scss';
#app {
  font-family: sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
  .main {
    margin: 15px;
  }

  .title {
    padding-bottom: 10px;
    padding-left: 15px;
  }


  /*a {*/
  /*  color: #339966;*/
  /*}*/


</style>
