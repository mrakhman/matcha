<template>
    <div class="main">

        <h3 class="title"> Register </h3>
        <b-container class="bv-example-row">
            <b-row><b-col xl="9">
                <b-form v-on:submit.prevent="submitRegister">

                    <!--                <ul v-if="errors.length">-->
                    <!--                    <li v-for="error in errors">{{ error }}</li>-->
                    <!--                </ul>-->

                    <!--                    <b-alert show v-if="errors.empty_input" variant="danger" dismissible>Empty input</b-alert>-->
                    <!--                    <b-alert show v-if="errors.password_repeat" variant="danger" dismissible>2 passwords</b-alert>-->


                    <b-alert v-model="errors.empty_input" variant="danger" dismissible>Empty input field</b-alert>
                    <b-alert v-model="errors.password_repeat" variant="danger" dismissible>2 passwords didn't match</b-alert>
                    <b-alert v-model="errors.spaces" variant="danger" dismissible>Don't use spaces</b-alert>
                    <b-alert v-model="errors.invalid_symbols" variant="danger" dismissible>Names and email must only include [a-z + A-Z] [0-9] and @</b-alert>
                    <b-alert v-model="errors.weak_password" variant="danger" dismissible>Password must be 8 chars long, include uppercase, lowercase, symbol, number</b-alert>
                    <b-alert v-model="errors.user_exists" variant="danger" dismissible>User already exists, email and username must be unique</b-alert>
                    <b-alert v-model="register_success_alert" variant="success" dismissible>User created! Check your email to activate account</b-alert>



                    <b-form-group
                            id="1"
                            label-cols-sm="2"
                            label-cols-lg="2"
                            label="First name"
                            label-for="input-horizontal"
                            required
                    >
                        <b-form-input required
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
                        <b-form-input required
                                v-model="form.last_name"
                                type="text"
                        ></b-form-input>
                    </b-form-group>
                    <b-form-group id="3" label-cols-sm="2" label-cols-lg="2" label="Email" label-for="input-horizontal" required>
                        <b-form-input required v-model="form.email" type="email"></b-form-input>
                        <b-form-text>You will receive email confirmation link</b-form-text>
                    </b-form-group>
                    <b-form-group id="4" label-cols-sm="2" label-cols-lg="2" label="Username" label-for="input-horizontal" required>
                        <b-form-input required v-model="form.username" type="text"></b-form-input>
                        <b-form-text>This will be your displayed name</b-form-text>
                    </b-form-group>
                    <b-form-group id="5" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
                        <b-form-input required v-model="form.password" type="password"></b-form-input>
                        <b-form-text>Password must be at least 8 chars long, include uppercase, lowercase, number</b-form-text>
                    </b-form-group>
                    <b-form-group id="6" label-cols-sm="2" label-cols-lg="2" label="Repeat password" label-for="input-horizontal" required>
                        <b-form-input required v-model="form.repeat_password" type="password"></b-form-input>
                        <b-form-text>Repeat your password</b-form-text>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Register</b-button>

                    <pre class="mt-3 mb-0">{{ form }}</pre>
                    <pre class="mt-3 mb-0">{{ errors }}</pre>
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
                    first_name: null,
                    last_name: null,
                    email: null,
                    username: null,
                    password: null,
                    repeat_password: null
                },
                errors: {
                    empty_input: false,
                    password_repeat: false,
                    invalid_symbols: false,
                    spaces: false,
                    weak_password: false,
                    user_exists: false
                },
                register_success_alert: false
                // errors: []

            }
        },
        methods: {
            validateRegister() {
                var has_error = 0;
                this.errors.empty_input = false;
                this.errors.password_repeat = false;
                this.errors.invalid_symbols = false;
                this.errors.spaces = false;
                this.errors.weak_password = false;
                this.errors.user_exists = false;
                this.register_success_alert = false;

                // Show alert on empty input
                if (!this.form.first_name || !this.form.last_name || !this.form.email || !this.form.username || !this.form.password || !this.form.repeat_password)
                {
                    this.errors.empty_input = true;
                    has_error = 1;
                }

                // Show alert if passwords don't match
                if (this.form.password !== this.form.repeat_password)
                {
                    this.errors.password_repeat = true;
                    has_error = 1;
                }

                // Show alert on space
                if (this.form.first_name.match(/( )/) || this.form.last_name.match(/( )/) || this.form.email.match(/( )/) || this.form.username.match(/( )/) || this.form.password.match(/( )/))
                {
                    this.errors.spaces = true;
                    has_error = 1;
                }

                // Show alert on unwanted characters
                var reg1 = /(?=.*[#$%^&+=§!*?><(){[\]}'";:~])/;
                if (this.form.first_name.match(reg1) || this.form.last_name.match(reg1) || this.form.email.match(reg1) || this.form.username.match(reg1))
                {
                    this.errors.invalid_symbols = true;
                    has_error = 1;
                }

                // Uncomment me later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                // // Show alert on weak password
                // var reg2 = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
                // if (!this.form.password.match(reg2))
                // {
                //     this.errors.weak_password = true;
                //     has_error = 1;
                // }

                if (has_error === 1)
                    return true;
                return false;

                // else
                //     return alert((JSON.stringify(this.form)))
            },

            submitRegister() {
                if (this.validateRegister())
                    return false;

                this.register_success_alert = false;

                axios.post(this.$root.API_URL + '/users/register', {
                    first_name: this.form.first_name,
                    last_name: this.form.last_name,
                    email: this.form.email,
                    username: this.form.username,
                    password: this.form.password
                }, {withCredentials: true})
                    .then(response => {
                        if(response.status === 200)
                        {
                            this.$notify({group: 'foo', type: 'success', title: 'User created', text: 'Check your email to activate account', duration: -1});
                            this.register_success_alert = true;
                            this.form.first_name = null;
                            this.form.last_name = null;
                            this.form.username = null;
                            this.form.email = null;
                            this.form.password = null;
                            this.form.repeat_password = null;

                        }
                        // TODO: console
                        console.log(response)
                })
                    .catch(error => {
                        if (error.response.status === 409) {
                            this.errors.user_exists = true;
                            this.$notify({group: 'foo', type: 'error', title: 'Error #409', text: 'User already exists, email and username must be unique', duration: -1});
                        }
                        // TODO: console
                        console.log(error)
                })
            },


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
