<template>
    <div>
        <b-container class="bv-example-row">
            <b-row>
                <b-col xl="9">
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
                    <b-button variant="primary">Register</b-button>

                    <pre class="mt-3 mb-0">{{ form }}</pre>

                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
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
        }
    }
</script>

<style lang="scss" scoped>
    @import '../assets/_custom.scss';
    @import '~bootstrap/scss/bootstrap.scss';
    @import '~bootstrap-vue/src/index.scss';

</style>
