<template>
    <div class="main">
        <pre>{{status}}</pre>
        <div v-if="status === true">
            <p>Your account is activated! You can now <a href="/login">login</a></p>
        </div>
<!--        <div v-else>-->
        <div>
            <p>Activation link is damaged or has expired, what should I do here? If person registers again - email already exists! I should send new activation link or delete account?</p>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "Activation.vue",
        data () {
            return {
                status: null,
                token: this.$route.params.token,
            }
        },
        methods: {
            getToken() {
                axios.get(this.$root.API_URL + '/users/activate/' + this.token, {withCredentials: true})
                    .then(response => {
                        if(response.status === 200)
                        {
                            this.status = true;
                            this.$notify({group: 'foo', type: 'success', title: 'Activated!', text: 'Your account is activated, you can now login', duration: -1});
                            // TODO: console
                            console.log(response)
                        }
                    })
                    .catch(error => {
                        this.status = false;
                        // TODO: console
                        console.log(error)
                    })
            },

        },
        created() {
            this.getToken();
        }
    }
</script>

<style scoped>

</style>
