<template>
    <div class="main"><b-row><b-col xl="6">
        <h3 class="title"> Forgot password </h3>
        <p> Enter email you registered your account with </p>
        <b-form-group id="3" label-cols-sm="2" label-cols-lg="2" label="Email" label-for="input-horizontal" required>
            <b-form-input v-model="form.email" type="email"></b-form-input>
            <b-form-text>You will receive password reset link</b-form-text>
        </b-form-group>
        <b-button type="sub mit" variant="primary" v-on:click="submitForgotPassword">Send</b-button>

    </b-col></b-row></div>
</template>



<script>

import axios from 'axios';

    export default {
        name: "ForgotPassword.vue",
        data() {
            return {
                form: {
                    email: ''
                }
            }
        },
        methods: {
            submitForgotPassword() {
                axios.post(this.$root.API_URL + "/api/auth/forgot_password", {
                    email: this.form.email
                }).then(response => {
                    console.log(response)
                }).catch(error => {
                    console.log(error)
                })
            }
        }
    }
</script>

<style scoped>

</style>