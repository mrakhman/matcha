<template>
    <div>
        <br><hr>
        <b-container>

        </b-container>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "CreateMessage.vue",
        props: ['username'],
        data() {
            return {
                users_list: [
                    {id: 1, username: 'koko', profile_image: "http://localhost:5000/images/20442157-329a-46df-8214-420d476b7b0c.png"},
                    {id: 2, username: 'losos', profile_image: "http://localhost:5000/images/20442157-329a-46df-8214-420d476b7b0c.png"},
                ]
            }
        },
        methods: {

        }
    }
</script>

<style scoped>

</style>
