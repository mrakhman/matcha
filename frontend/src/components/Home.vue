<template>
    <div class="main">
        <h3>Welcome home!</h3>
        <p>You can:</p>
        <p>View and edit your <router-link v-bind:to="'/my_profile'">profile</router-link> and personal details in settings tab</p>
        <p>Find other users in <router-link v-bind:to="'/search'">search</router-link>, filter results by age gap, fame rating, distance or selected tags</p>
        <p>Allow us access your <router-link v-bind:to="'/search'">geolocation</router-link> or find your address to get most accurate data about closest users</p>
        <p>Remember: you are invisible for other users until you have a  <router-link v-bind:to="'/my_profile'">profile image</router-link> and main profile info</p>
        <p>In <router-link v-bind:to="'/search'">search users list</router-link> visit other users' profile pages to like, block, report them as fake or chat with them</p>
        <p>When another user likes you back, you will see "Go to chat!" button on their <router-link v-bind:to="'/users/48'">profile page</router-link> (just an example)</p>
        <p>All your <router-link v-bind:to="'/chat'">chats are here</router-link>. You can chat only with mutually liked users. If one of you unliked another, chat history will be still accessible</p>
        <p>You will receive real-time <router-link v-bind:to="'/notifications'">notifications</router-link> about likes, unlikes, new messages and profile views</p>
        <p>We save <router-link v-bind:to="'/history'">history</router-link> of profiles that you visited. Click the profile link to visit user's page</p>
    </div>
</template>

<script>
    export default {
        name: "Home.vue",
        data () {
            return {
            }
        },
        methods: {}
    }
</script>

<style scoped>

</style>
