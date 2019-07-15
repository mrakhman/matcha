<template>
    <div class="main">
        <h3 class="title"> Login </h3>
        <b-row><b-col xl="7">
            <b-alert v-model="input_error" variant="danger" dismissible>Empty input field</b-alert>
            <b-alert v-model="bad_request" variant="danger" dismissible>User does not exist</b-alert>
            <b-alert v-model="forbidden" variant="danger" dismissible>Click activation link in your email before login</b-alert>
            <b-alert v-model="unauthorized" variant="danger" dismissible>Wrong password or user doesn't exist</b-alert>

            <b-alert v-model="login_success" variant="success" dismissible>User logged in!</b-alert>


            <router-link id="forgot" v-bind:to="'/forgot_password'">Forgot password?</router-link>

            <b-form v-on:submit.prevent="login">
                <b-form-group id="login_username" label-cols-sm="2" label-cols-lg="2" label="Username" label-for="input-horizontal" required>
                    <b-form-input required v-model="form.username" type="text"></b-form-input>
                    <b-form-text>This is your displayed name</b-form-text>
                </b-form-group>
                    <b-form-group id="login_password" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
                    <b-form-input required v-model="form.password" type="password"></b-form-input>
                </b-form-group>


                <b-button type="submit" variant="outline-primary">Login</b-button>
            </b-form>
        </b-col></b-row></div>
</template>

<script>
    import axios from 'axios';
    // import {Auth} from "../auth";
    export default {
        name: "Login.vue",
        data () {
            return {
                // auth: this.$root.$data.Auth,
                form: {
                    username: '',
                    password: ''
                },
                login_success: false,
                input_error: false,
                unauthorized: false,
                bad_request: false,
                forbidden: false,

                errors: [] // Can be deleted
            }
        },
        methods: {
            login() {
                // Show alert on empty input
                if (!this.form.username || !this.form.password)
                    return this.input_error = true;

                // If no error on front - Axios requests
                axios.post(this.$root.API_URL + '/auth/login', {
                    username: this.form.username,
                    password: this.form.password
                }, {withCredentials: true})
                    .then(() => {
                        // console.log(response);

                        // Nested Axios request - whoami data
                        axios.get(this.$root.API_URL + '/users/me', {withCredentials: true})
                            .then(response => {
                                // console.log(response);
                                localStorage.setItem('user_id', response.data.user.id);
                                localStorage.setItem('user', JSON.stringify(response.data.user));
                                this.$router.push('/my_profile');
                                this.$router.go();
                            })
                            // TODO: console
                            // eslint-disable-next-line
                            .catch(error => {
                                console.log(error);

                            });


                        // eslint-disable-next-line
                        // this.login_success = true;

                        // Auth.login();
                        // Auth.loggedIn = true;
                        // this.auth.loggedIn = true;

                        // this.$router.push('/my_profile');
                        // this.$router.go();  // Заглушка - reload после перехода на /my_profile, так как сложно здесь использовать $emit и передавать факт логина в App.vue

                        // localStorage.setItem('auth', JSON.stringify(response.data.data));
                        // this.$root.auth = response.data.data /* [2:20:56] https://www.youtube.com/watch?v=L5oaI-C8Dhc&t=2494s */
                })
                    .catch(error => {
                        if (error.response.status === 401) {
                            this.unauthorized = true;
                        }
                        if (error.response.status === 400) {
                            this.bad_request = true;
                        }
                        if (error.response.status === 403) {
                            this.forbidden = true;
                        }
                });
            },



        }
    }
</script>

<style scoped>
    #forgot {
        margin: 20px;
    }
</style>
