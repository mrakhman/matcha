<template>
    <div>
        <b-form inline v-on:submit.prevent="logout">
            <b-button type="submit" variant="outline-primary">Logout</b-button>
        </b-form>
    </div>
</template>

<script>
    export default {
        name: "Logout.vue",
        data () {
            return {
            }
        },
        methods: {
            logout() {
                this.$root.axios.post('/auth/logout', {}, {withCredentials: true})
                    .then(response => {
                        if (response.status === 200)
                        {
                            this.$store.commit('logout');
                            this.$router.push('/login');
                        }
                    })
                    .catch(() => {});


            }
        }
    }
</script>

<style scoped>

</style>
