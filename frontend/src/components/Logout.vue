<template>
    <div>
        <b-form inline v-on:submit.prevent="logout">
            <b-button type="submit" variant="outline-primary">Logout</b-button>
        </b-form>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Logout.vue",
        data () {
            return {
            }
        },
        methods: {
            logout() {
                axios.post(this.$root.API_URL + '/auth/logout', {}, {withCredentials: true})
                    .then(response => {
                        if (response.status === 200)
                        {
                            localStorage.removeItem('user');
                            localStorage.removeItem('user_id');
                            this.$router.push('/login');
                            this.$router.go(0); // Need it because we stopped $emit action to App data.session
                        }
                    })
                    .catch(() => {});


            }
        }
    }
</script>

<style scoped>

</style>
