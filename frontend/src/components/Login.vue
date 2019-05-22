<template>
    <div class="main">
        <h3 class="title"> Login </h3>
        <b-row><b-col xl="7">
            <b-alert v-model="input_error" variant="danger" dismissible>Empty input field</b-alert>
            <b-alert show variant="danger">User does not exist</b-alert>
            <b-alert show variant="danger">Click the link in your email before login</b-alert>
            <b-alert show variant="danger">Wrong password or email not confirmed</b-alert>

            <b-alert v-model="login_success" variant="success" dismissible>User logged in!</b-alert>


            <a id="forgot" href="/forgot_password">Forgot password?</a>

            <b-form v-on:submit.prevent="login">
                <b-form-group id="login_username" label-cols-sm="2" label-cols-lg="2" label="Username" label-for="input-horizontal" required>
                    <b-form-input v-model="form.username" type="text"></b-form-input>
                    <b-form-text>This is your displayed name</b-form-text>
                </b-form-group>
                    <b-form-group id="login_password" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
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
                },
                login_success: false,
                input_error: false
            }
        },
        methods: {
            login() {
                // Show alert on empty input
                if (!this.form.username || !this.form.password)
                    return this.input_error = true;

                axios.post(this.$root.API_URL + '/auth/login', {
                    username: this.form.username,
                    password: this.form.password
                }, {withCredentials: true})
                    .then(response => {
                        // TODO: console
                        // eslint-disable-next-line
                        // this.login_success = true;

                        Auth.login();

                        this.$router.push('/my_profile');
                        this.$router.go();  // Заглушка - reload после перехода на /my_profile, так как сложно здесь использовать $emit и передавать факт логина в App.vue

                        // localStorage.setItem('auth', JSON.stringify(response.data.data));
                        // this.$root.auth = response.data.data /* [2:20:56] https://www.youtube.com/watch?v=L5oaI-C8Dhc&t=2494s */
                })
                    .catch(error => {
                        // TODO: console
                        // eslint-disable-next-line
                        alert('Couldn`t login')
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
