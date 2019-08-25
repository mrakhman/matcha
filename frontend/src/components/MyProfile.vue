<template>
<div class="main">
    <h3 class="title"> My profile </h3>
    <p v-if="user.online" class="text-success ml-3"><b> Online </b></p>
    <p v-else class="text-danger ml-3"><b> Offline <br> <small v-if="user.last_connection">
        Last seen: {{user.last_connection | moment('timezone', "Europe/Paris", 'LLLL')}}</small></b></p>
    <b-tabs content-class="mt-3">
        <b-tab title="About me" active>
            <AboutMe />
        </b-tab>

        <b-tab title="Settings">
            <Settings />
        </b-tab>
    </b-tabs>
</div>
</template>

<script>
    import AboutMe from "./AboutMe";
    import Settings from "./Settings";
    import {mapState} from 'vuex'

    export default {
        name: "MyProfile.vue",
        components: {
            AboutMe,
            Settings
        },
        computed: mapState({
            user: state => state.user,
        })
    }
</script>

<style scoped lang="scss">
    @import '../assets/_custom.scss';
    @import '~bootstrap/scss/bootstrap.scss';
    @import '~bootstrap-vue/src/index.scss';

    #profile_image {
        padding: 10px;
    }

    .profile_img {
        margin-right: 5px;
    }

    .card_section {
        margin-bottom: 20px;
    }

    .title {
        padding-bottom: 20px;
        padding-left: 15px;
    }
</style>



