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
        methods: {
            logout() {
                // remove user from local storage to log user out
                localStorage.removeItem('user');
            }
        }
    }
</script>

<style scoped>

</style>
