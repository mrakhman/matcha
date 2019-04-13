
<template>
  <div id="app">
    <AddTodo v-on:add-todo="addTodo"/>
    <Todos v-bind:todos="todos" v-on:del-todo="deleteTodo"/>
  </div>
</template>

<script>
// import HelloWorld from './components/Hello World.vue'

import Todos from "./components/Todos";
import AddTodo from "./components/AddTodo";
import axios from 'axios';

export default {
  name: 'app',
  components: {
      Todos,
      AddTodo
  },
    data() {
      return {
          todos: []
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

<style>
#app {
  font-family: Sans-Serif;
  /*-webkit-font-smoothing: antialiased;*/
  /*-moz-osx-font-smoothing: grayscale;*/
  /*text-align: center;*/
  /*color: #2c3e50;*/
  /*margin-top: 60px;*/
}
</style>
