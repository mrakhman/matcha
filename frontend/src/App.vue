<template>
  <div id="app">
    <AppHeader/>
    <router-view></router-view>
      <notifications group="foo" />
    <Footer/>
  </div>
</template>

<script>

import Header from "./components/Header";
import Footer from "./components/Footer";
import { mapState } from 'vuex';

export default {
  name: 'app',
  components: {
      AppHeader: Header,
      Footer,
  },
  computed: mapState(['logged_in']),
  watch: {
    logged_in(newValue, oldValue) {
      if (newValue === oldValue)
        return ;
      if (newValue) {
        this.$connect()
      } else {
        this.$disconnect()
      }
    }
  }
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

</style>
