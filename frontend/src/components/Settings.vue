<template>
    <div>
        <b-container class="bv-example-row"><b-row><b-col xl="8">
            <b-alert v-model="alerts.empty_input" variant="danger" dismissible>Empty input field</b-alert>
            <b-alert v-model="alerts.empty_old_password" variant="danger" dismissible>Enter old password</b-alert>
            <b-alert v-model="alerts.password_repeat" variant="danger" dismissible>2 passwords didn't match</b-alert>
            <b-alert v-model="alerts.invalid_symbols" variant="danger" dismissible>Names and email must only include [a-z + A-Z] [0-9] and @</b-alert>
            <b-alert v-model="alerts.spaces" variant="danger" dismissible>Don't use spaces</b-alert>
            <b-alert v-model="alerts.weak_password" variant="danger" dismissible>Password must be 8 chars long, include uppercase, lowercase, number</b-alert>

            <b-alert v-model="alerts.names_saved" variant="success" dismissible>Name settings are saved!</b-alert>


            <b-form v-on:submit.prevent="submitChangeNames">
                <b-card class="card_section" bg-variant="light">
                    <h4 align="center">Name</h4>
                    <b-form-group id="1" label-cols-sm="2" label-cols-lg="2" label="First name" label-for="input-horizontal">
                        <b-form-input
                                v-model="form_edit.first_name"
                                type="text"
                                v-bind:placeholder="user_details.first_name"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="2" label-cols-sm="2" label-cols-lg="2" label="Last name" label-for="input-horizontal">
                        <b-form-input
                                v-model="form_edit.last_name"
                                type="text"
                                v-bind:placeholder="user_details.last_name"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="3" label-cols-sm="2" label-cols-lg="2" label="Username" label-for="input-horizontal">
                        <b-form-input
                                v-model="form_edit.username"
                                type="text"
                                v-bind:placeholder="user_details.username"
                        ></b-form-input>
                        <b-form-text>This will be your displayed name</b-form-text>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Save</b-button>
                </b-card>
            </b-form>

            <b-alert v-model="alerts.unauthorized" variant="danger" dismissible>Wrong password</b-alert>
            <b-alert v-model="alerts.email_saved" variant="success" dismissible>Email will be changed after you confirm it, check your email and press activation link!</b-alert>

            <b-form v-on:submit.prevent="submitChangeEmail">
                <b-card class="card_section" bg-variant="light">
                    <h4 align="center">New email</h4>
                    <b-form-group id="4" label-cols-sm="2" label-cols-lg="2" label="Email" label-for="input-horizontal" required>
                        <b-form-input required v-model="form_edit.email" type="email"></b-form-input>
                        <b-form-text>You will receive email confirmation link</b-form-text>
                    </b-form-group>

                    <b-form-group id="5" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
                        <b-form-input required v-model="form_edit.email_password" type="password"></b-form-input>
                        <b-form-text>Confirm with your password</b-form-text>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Save</b-button>
                </b-card>
            </b-form>

            <b-form v-on:submit.prevent="submitChangePassword">
                <b-card class="card_section" bg-variant="light">
                    <h4 align="center">Password</h4>
                    <b-form-group id="6" label-cols-sm="2" label-cols-lg="2" label="Old password" label-for="input-horizontal" required>
                        <b-form-input required v-model="form_edit.old_password" type="password"></b-form-input>
                    </b-form-group>

                    <b-form-group id="7" label-cols-sm="2" label-cols-lg="2" label="New password" label-for="input-horizontal" required>
                        <b-form-input required v-model="form_edit.new_password" type="password" v-bind:disabled="form_edit.old_password.length > 0 ? false : true"></b-form-input>
                        <b-form-text>Password must be at least 8 chars long, include uppercase, lowercase, symbol, number</b-form-text>
                    </b-form-group>

                    <b-form-group id="8" label-cols-sm="2" label-cols-lg="2" label="Repeat password" label-for="input-horizontal" required>
                        <b-form-input required v-model="form_edit.repeat_password" type="password" v-bind:disabled="form_edit.old_password.length > 0 ? false : true"></b-form-input>
                        <b-form-text>Repeat your new password</b-form-text>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Save</b-button>
                </b-card>
            </b-form>
        </b-col></b-row></b-container>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Settings.vue",
        props: {
            form_edit: Object,
            alerts: Object,
            user_details: Object
        },
        methods: {
            submitChangeNames() {
                // Show alert on empty input
                // I let 2 out of 3 be empty cause I might want to change just one. On backend: if field is empty - keep old value
                if (!this.form_edit.first_name && !this.form_edit.last_name && !this.form_edit.username)
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Empty input field', duration: -1});
                    return this.alerts.empty_input = true;

                }

                // Show alert on space
                if (this.form_edit.first_name.match(/( )/) || this.form_edit.last_name.match(/( )/) || this.form_edit.username.match(/( )/))
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Don\'t use spaces', duration: -1});
                    return this.alerts.spaces = true;
                }

                // Show alert on unwanted characters
                var reg1 = /(?=.*[#$%^&+=§!*?><(){[\]}'";:~])/;
                if (this.form_edit.first_name.match(reg1) || this.form_edit.last_name.match(reg1) || this.form_edit.username.match(reg1))
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Names must only include [a-z + A-Z] [0-9] and @', duration: -1});
                    return this.alerts.invalid_symbols = true;
                }

                axios.post(this.$root.API_URL + '/users/edit_names', {
                    first_name: this.form_edit.first_name,
                    last_name: this.form_edit.last_name,
                    username: this.form_edit.username,
                }, {withCredentials: true})
                    .then(response => {
                        if(response.status === 200)
                        {
                            this.$notify({group: 'foo', type: 'success', title: 'Saved!', text: 'Name settings are saved', duration: 1000});
                            this.alerts.names_saved = true;
                        }
                        // console.log(response)
                    })
                    .catch(error => {
                        if (error.response.status === 409) {
                            this.$notify({group: 'foo', type: 'error', title: 'Error #409', text: 'Another user has this username', duration: -1});
                        }
                        // TODO: console
                        if (error.response.status !== 401 && error.response.status !== 409)
                            console.log(error)
                    })
            },

            submitChangeEmail() {
                // Show alert on empty input
                if (!this.form_edit.email || !this.form_edit.email_password)
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Empty input field', duration: -1});
                    return this.alerts.empty_input = true;
                }

                // Show alert on space
                if (this.form_edit.email.match(/( )/) || this.form_edit.email_password.match(/( )/))
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Don\'t use spaces', duration: -1});
                    return this.alerts.spaces = true;
                }

                // Show alert on unwanted characters
                var reg1 = /(?=.*[#$%^&+=§!*?><(){[\]}'";:~])/;
                if (this.form_edit.email.match(reg1))
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Email must only include [a-z + A-Z] [0-9] and @', duration: -1});
                    return this.alerts.invalid_symbols = true;
                }

                axios.post(this.$root.API_URL + '/users/edit_email', {
                    email: this.form_edit.email,
                    password: this.form_edit.email_password
                }, {withCredentials: true})
                    .then(response => {
                        if(response.status === 200)
                        {
                            this.$notify({group: 'foo', type: 'success', title: 'Saved!', text: 'Email will be changed after you confirm it, check your email and press activation link!', duration: -1});
                            this.alerts.email_saved = true;
                        }
                        // console.log(response)
                    })
                    .catch(error => {
                        if (error.response.status === 401) {
                            this.$notify({group: 'foo', type: 'error', title: 'Error #401', text: 'Unauthorized - wrong password', duration: -1});
                            this.alerts.unauthorized = true;
                        }
                        if (error.response.status === 409) {
                            this.$notify({group: 'foo', type: 'error', title: 'Error #409', text: 'Another user has this email', duration: -1});
                        }
                        // TODO: console
                        if (error.response.status !== 401 && error.response.status !== 409)
                            console.log(error)
                    })
            },

            submitChangePassword() {
                // Empty old password
                if (!this.form_edit.old_password)
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Empty old password', duration: -1});
                    return this.alerts.empty_old_password = true;
                }

                // Show alert on empty input
                if (!this.form_edit.new_password || !this.form_edit.repeat_password)
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Empty input field', duration: -1});
                    return this.alerts.empty_input = true;
                }

                // Show alert if passwords don't match
                if (this.form_edit.new_password !== this.form_edit.repeat_password)
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: '2 passwords didn\'t match', duration: -1});
                    return this.alerts.password_repeat = true;
                }

                // Show alert on space
                if (this.form_edit.new_password.match(/( )/))
                {
                    this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Don\'t use spaces', duration: -1});
                    return this.alerts.spaces = true;
                }

                // TODO: Uncomment me later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                // // Show alert on weak password
                // var reg2 = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
                // if (!this.form_edit.new_password.match(reg2))
                // {
                //     this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Weak password: password must be at least 8 chars long, include uppercase, lowercase, symbol, number', duration: -1});
                //     return this.alerts.weak_password = true;
                // }

                axios.post(this.$root.API_URL + '/users/edit_password', {
                    old_password: this.form_edit.old_password,
                    new_password: this.form_edit.new_password
                }, {withCredentials: true})
                    .then(response => {
                        if(response.status === 200)
                        {
                            this.$notify({group: 'foo', type: 'success', title: 'Saved!', text: 'Password changed!', duration: -1});
                        }
                        // console.log(response)
                    })
                    .catch(error => {
                        if (error.response.status === 401) {
                            this.$notify({group: 'foo', type: 'error', title: 'Error #401', text: 'Unauthorized - wrong old password', duration: -1});
                        }
                        // TODO: console
                        if (error.response.status !== 401)
                            console.log(error)
                    })
            },

        }
    }
</script>

<style scoped>
    .card_section {
        margin-bottom: 20px;
    }


</style>
