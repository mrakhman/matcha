<template>
    <div>
        <b-form inline v-on:submit.prevent="logout">
            <b-button v-on:submit.prevent="logout" type="submit" variant="outline-primary">Logout</b-button>
        </b-form>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: "Logout.vue",
        methods: {
            logout() {
                axios.post(this.$root.API_URL + '/auth/logout', {}, {withCredentials: true})
                    .then(response => {
                        // TODO: console
                        this.$emit('del_session');
                        this.$router.push('/login');

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
