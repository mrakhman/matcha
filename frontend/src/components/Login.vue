<template>
    <div class="main">
        <h3 class="title"> Login </h3>
        <b-row><b-col xl="7">
        <b-alert show variant="danger">Empty input field</b-alert>
        <b-alert show variant="danger">User does not exist</b-alert>
        <b-alert show variant="danger">Click the link in your email before login</b-alert>
        <b-alert show variant="danger">Wrong password or email not confirmed</b-alert>

            <a id="forgot" href="/forgot_password">Forgot password?</a>

            <b-form v-on:submit.prevent="login">
            <b-form-group id="4" label-cols-sm="2" label-cols-lg="2" label="Username" label-for="input-horizontal" required>
                <b-form-input v-model="form.username" type="text"></b-form-input>
                <b-form-text>This is your displayed name</b-form-text>
            </b-form-group>
                <b-form-group id="5" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
                <b-form-input v-model="form.password" type="password"></b-form-input>
            </b-form-group>


            <b-button type="submit" variant="outline-primary">Login</b-button>
        </b-form>
        </b-col></b-row></div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: "Login.vue",
        data () {
            return {
                form: {
                    username: '',
                    password: ''
                }
            }
        },
        methods: {
            login() {
                alert((JSON.stringify(this.form)))
            },

            login_2() {
                axios.post('http://localhost:5000', {
                    first_name: this.form.first_name,
                    last_name: this.form.last_name,
                    email: this.form.email,
                    username: this.form.username,
                    password: this.form.password
                })
                    .then(response => {
                        localStorage.setItem('auth', JSON.stringify(response.data.data));
                        this.$root.auth = response.data.data /* [2:20:56] https://www.youtube.com/watch?v=L5oaI-C8Dhc&t=2494s */
                })
                    .catch(error => {
                    console.log(error)
                })
            }
        }
    }
</script>

<style scoped>
    #forgot {
        margin: 20px;
    }
</style>
