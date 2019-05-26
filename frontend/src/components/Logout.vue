<template>
    <div>
        <b-form inline v-on:submit.prevent="logout">
            <b-button type="submit" variant="outline-primary">Logout</b-button>
        </b-form>
    </div>
</template>

<script>
    import axios from 'axios';
    // import {Auth} from "../auth";
    export default {
        name: "Logout.vue",
        data () {
            return {
                // auth: this.$root.$data.Auth
            }
        },
        methods: {
            logout() {
                axios.post(this.$root.API_URL + '/auth/logout', {}, {withCredentials: true})
                    .then(response => {
                        // TODO: console
                        // this.$emit('del_session');
                        console.log(response);
                        if (response.statusText === 'OK')
                        {
                            // Auth.loggedIn = false;
                            // this.auth.loggedIn = false;
                            localStorage.removeItem('user');
                            localStorage.removeItem('user_id');
                            this.$router.push('/login');
                            this.$router.go(); // Need it because we stopped $emit action to App data.session
                        }


                        // eslint-disable-next-line
                    })
                    .catch(error => {
                        // TODO: console
                        // eslint-disable-next-line
                        alert('Couldn`t logout')
                    });


            }
        }
    }
</script>

<style scoped>

</style>
