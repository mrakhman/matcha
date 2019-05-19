<template>
  <div id="app">
    <Header/>
    <router-view></router-view><!-- Main routing enter point -->
<!--    <div class="main">-->
<!--      <Register/>-->
      <br><hr>
<!--      <MyProfile/>-->
<!--    </div>-->


    <Footer/>

    <Header
            :user_id="user_id"
            :first_name="first_name"
            :last_name="last_name"
            :username="username"
    />
  </div>
</template>

<script>
// import HelloWorld from './components/Hello World.vue'

// import Todos from "./components/Todos";
// import AddTodo from "./components/AddTodo";
import axios from 'axios';
import Header from "./components/Header";
import Footer from "./components/Footer";
// import Register from "./components/Register";
// import MyProfile from "./components/MyProfile";
// import './assets/_custom.scss'

export default {
  name: 'app',
  components: {
    Header,
    Footer
    // Register
    // MyProfile
  },
    data() {
      return {
        todos: [],
        session: {
          'user_id': null,
          'context': {
            'first_name': '',
            'last_name': '',
            'username': ''
          }
        }
      }
    },

    methods: {
      deleteTodo(id) {
          axios.delete(`https://jsonplaceholder.typicode.com/todos/${id}`)
              .then(res => this.todos = this.todos.filter(todo => todo.id !== id))
              .catch(err => console.log(err));
          // this.todos = this.todos.filter(todo => todo.id !== id);
      },

      addTodo(newTodo) {
          const {title, completed} = newTodo;

          axios.post('https://jsonplaceholder.typicode.com/todos', {
              title,
              completed
          })
              .then(res => this.todos = [...this.todos, res.data])
              .catch(err => console.log(err));

          // this.todos = [...this.todos, newTodo];
      }
    },
    created() {
      axios.get('https://jsonplaceholder.typicode.com/todos?_limit=5')
        .then(res => this.todos = res.data)
        .catch(err => console.log(err));
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


  /*a {*/
  /*  color: #339966;*/
  /*}*/


</style>
