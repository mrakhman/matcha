<template>
    <div>
        <b-container class="bv-example-row"><b-row><b-col xl="8">
            <b-alert v-model="alerts.empty_input" variant="danger" dismissible>Empty input field</b-alert>
            <b-alert v-model="alerts.empty_old_password" variant="danger" dismissible>Enter old password</b-alert>
            <b-alert v-model="alerts.password_repeat" variant="danger" dismissible>2 passwords didn't match</b-alert>
            <b-alert v-model="alerts.invalid_symbols" variant="danger" dismissible>Names and email must only include [a-z + A-Z] [0-9] and @</b-alert>
            <b-alert v-model="alerts.spaces" variant="danger" dismissible>Don't use spaces</b-alert>
            <b-alert v-model="alerts.weak_password" variant="danger" dismissible>Password must be 8 chars long, include uppercase, lowercase, number</b-alert>

            <b-form v-on:submit.prevent="submitChangeNames">
                <b-card class="card_section" bg-variant="light">
                    <h4 align="center">Name</h4>
                    <b-form-group id="1" label-cols-sm="2" label-cols-lg="2" label="First name" label-for="input-horizontal" required>
                        <b-form-input
                                v-model="form_edit.first_name"
                                type="text"
                                v-bind:placeholder="user_details.first_name"

                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="2" label-cols-sm="2" label-cols-lg="2" label="Last name" label-for="input-horizontal" required>
                        <b-form-input
                                v-model="form_edit.last_name"
                                type="text"
                                v-bind:placeholder="user_details.last_name"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="3" label-cols-sm="2" label-cols-lg="2" label="Username" label-for="input-horizontal" required>
                        <b-form-input v-model="form_edit.username" type="text"></b-form-input>
                        <b-form-text>This will be your displayed name</b-form-text>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Save</b-button>
                </b-card>
            </b-form>

            <b-form v-on:submit.prevent="submitChangeEmail">
                <b-card class="card_section" bg-variant="light">
                    <h4 align="center">Email</h4>
                    <b-form-group id="4" label-cols-sm="2" label-cols-lg="2" label="Email" label-for="input-horizontal" required>
                        <b-form-input required v-model="form_edit.email" type="email"></b-form-input>
                        <b-form-text>You will receive email confirmation link</b-form-text>
                    </b-form-group>

                    <b-form-group id="5" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
                        <b-form-input required v-model="form_edit.password" type="password"></b-form-input>
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
                        <b-form-input required v-model="form_edit.password" type="password" disabled></b-form-input>
                        <b-form-text>Password must be at least 8 chars long, include uppercase, lowercase, symbol, number</b-form-text>
                    </b-form-group>

                    <b-form-group id="8" label-cols-sm="2" label-cols-lg="2" label="Repeat password" label-for="input-horizontal" required>
                        <b-form-input required v-model="form_edit.repeat_password" type="password" disabled></b-form-input>
                        <b-form-text>Repeat your new password</b-form-text>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Save</b-button>
                </b-card>
            </b-form>

            <pre class="mt-3 mb-0">{{ form_edit }}</pre>



        </b-col></b-row></b-container>
    </div>
</template>

<script>
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
                    return this.alerts.empty_input = true;
                }

                // Show alert on space
                if (this.form_edit.first_name.match(/( )/) || this.form_edit.last_name.match(/( )/) || this.form_edit.username.match(/( )/))
                {
                    return this.alerts.spaces = true;
                }

                // Show alert on unwanted characters
                var reg1 = /(?=.*[#$%^&+=§!*?><(){[\]}'";:~])/;
                if (this.form_edit.first_name.match(reg1) || this.form_edit.last_name.match(reg1) || this.form_edit.username.match(reg1))
                {
                    return this.alerts.invalid_symbols = true;
                }
            },

            submitChangeEmail() {
                // Show alert on empty input
                if (!this.form_edit.email || !this.form_edit.password)
                {
                    return this.alerts.empty_input = true;
                }

                // Show alert on space
                if (this.form_edit.email.match(/( )/) || this.form_edit.password.match(/( )/))
                {
                    return this.alerts.spaces = true;
                }

                // Show alert on unwanted characters
                var reg1 = /(?=.*[#$%^&+=§!*?><(){[\]}'";:~])/;
                if (this.form_edit.email.match(reg1))
                {
                    return this.alerts.invalid_symbols = true;
                }
            },

            submitChangePassword() {
                // Empty old password
                if (!this.form_edit.old_password)
                {
                    return this.alerts.empty_old_password = true;
                }

                // Show alert on empty input
                if (!this.form_edit.password || !this.form_edit.repeat_password)
                {
                    return this.alerts.empty_input = true;
                }

                // Show alert if passwords don't match
                if (this.form_edit.password !== this.form_edit.repeat_password)
                    return this.alerts.password_repeat = true;

                // Show alert on space
                if (this.form_edit.password.match(/( )/))
                {
                    return this.alerts.spaces = true;
                }

                // Uncomment me later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                // // Show alert on weak password
                // var reg2 = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
                // if (!this.form_edit.password.match(reg2))
                // {
                //     return this.alerts.weak_password = true;
                // }

                else
                    alert((JSON.stringify(this.form)))
            }
        }
    }
</script>

<style scoped>
    .card_section {
        margin-bottom: 20px;
    }


</style>
