<template>
    <div>
        <b-form inline v-on:submit.prevent="logout">
            <b-button v-on:submit.prevent="logout" type="submit" variant="outline-primary">Logout</b-button>
        </b-form>
    </div>
</template>

<script>
    import axios from 'axios';
    import {Auth} from "../auth";
    export default {
        name: "Logout.vue",
        methods: {
            logout() {
                axios.post(this.$root.API_URL + '/auth/logout', {}, {withCredentials: true})
                    .then(response => {
                        // TODO: console
                        // this.$emit('del_session');
                        console.log(response);
                        if (response.statusText === 'OK')
                        {
                            Auth.logout();
                            this.$router.push('/');
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
