<template>
    <div class="main"><b-row><b-col xl="5">
        <h3 class="title"> Forgot password </h3>
        <p> Enter email you registered your account with </p>
        <form v-on:submit.prevent="forgotPassword">
            <b-form-group id="3" label-cols-sm="2" label-cols-lg="2" label="Email" label-for="input-horizontal">
                <b-form-input required v-model="email" type="email"></b-form-input>
                <b-form-text>You will receive password reset link</b-form-text>
            </b-form-group>
            <p class="text-success" v-if="email_sent === true">Check your email!</p>
            <b-button type="submit" variant="primary">Send</b-button>
        </form>
    </b-col></b-row></div>
</template>



<script>

    export default {
        name: "ForgotPassword.vue",
        data() {
            return {
                email: null,
                email_sent: false
            }
        },
        methods: {
            forgotPassword() {
                this.email_sent = false;
                this.$root.axios.post('/recovery/password', {
                    email: this.email,
                }, {withCredentials: true})
                    .then(response => {
                        if(response.status === 200)
                        {
                            this.$notify({group: 'foo', type: 'success', title: 'Sent', text: 'Link to reset your password is sent to your email', duration: 3000});
                            this.email = null;
                            this.email_sent = true;
                        }
                    })
                    .catch(error => {
                        if (error.response.status === 404) {
                            this.$notify({group: 'foo', type: 'error', title: 'Error #404', text: 'User with this email doesn\'t exist', duration: 4000});
                        }
                    })
            }
        }
    }
</script>

<style scoped>

</style>
