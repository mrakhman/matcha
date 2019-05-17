<template>
    <div class="main">
        <h3 class="title"> Register </h3>
        <b-container class="bv-example-row">
            <b-row><b-col xl="9">
                <b-alert show variant="danger">Empty input field</b-alert>
                <b-alert show variant="danger">2 passwords didn't match</b-alert>
                <b-alert show variant="danger">Invalid input characters</b-alert>
                <b-alert show variant="danger">Don't use spaces</b-alert>
                <b-alert show variant="danger">Username and email must only include [a-z + A-Z] [0-9] and @</b-alert>
                <b-alert show variant="danger">Password must be 8 chars long, include uppercase, lowercase, symbol, number</b-alert>
                <b-alert show variant="danger">User already exists</b-alert>

                <b-alert show variant="success">User created! Check your email to activate account</b-alert>
                <b-form v-on:submit.prevent="submitRegister">
                    <b-form-group
                            id="1"
                            label-cols-sm="2"
                            label-cols-lg="2"
                            label="First name"
                            label-for="input-horizontal"
                            required
                    >
                        <b-form-input
                                v-model="form.first_name"
                                type="text"
                        ></b-form-input>
                    </b-form-group>
                    <b-form-group
                            id="2"
                            label-cols-sm="2"
                            label-cols-lg="2"
                            label="Last name"
                            label-for="input-horizontal" required
                    >
                        <b-form-input
                                v-model="form.last_name"
                                type="text"
                        ></b-form-input>
                    </b-form-group>
                    <b-form-group id="3" label-cols-sm="2" label-cols-lg="2" label="Email" label-for="input-horizontal" required>
                        <b-form-input v-model="form.email" type="email"></b-form-input>
                        <b-form-text>You will receive email confirmation link</b-form-text>
                    </b-form-group>
                    <b-form-group id="4" label-cols-sm="2" label-cols-lg="2" label="Username" label-for="input-horizontal" required>
                        <b-form-input v-model="form.username" type="text"></b-form-input>
                        <b-form-text>This will be your displayed name</b-form-text>
                    </b-form-group>
                    <b-form-group id="5" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
                        <b-form-input v-model="form.password" type="password"></b-form-input>
                        <b-form-text>Password must be at least 8 chars long, include uppercase, lowercase, symbol, number</b-form-text>
                    </b-form-group>
                    <b-form-group id="6" label-cols-sm="2" label-cols-lg="2" label="Repeat password" label-for="input-horizontal" required>
                        <b-form-input type="password"></b-form-input>
                        <b-form-text>Repeat your password</b-form-text>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Register</b-button>

                    <pre class="mt-3 mb-0">{{ form }}</pre>
                </b-form>
            </b-col></b-row>
        </b-container>
    </div>
</template>

<script>

import axios from 'axios';

    export default {
        name: "Register.vue",
        data() {
            return {
                form: {
                    first_name: '',
                    last_name: '',
                    email: '',
                    username: '',
                    password: ''
                }
            }
        },
        methods: {
            // submitRegister() {
            //     axios.post('http://localhost:8080', {
            //         first_name: this.form.first_name,
            //         last_name: this.form.last_name,
            //         email: this.form.email,
            //         username: this.form.username,
            //         password: this.form.password
            //     }).then(response => {
            //         console.log(response)
            //     }).catch(error => {
            //         console.log(error)
            //     })
            // },
            submitRegister() {
                alert((JSON.stringify(this.form)))
            }
        }
    }

</script>

<style lang="scss" scoped>
    @import '../assets/_custom.scss';
    @import '~bootstrap/scss/bootstrap.scss';
    @import '~bootstrap-vue/src/index.scss';


    .title {
        padding-bottom: 20px;
        padding-left: 15px;
    }

</style>
