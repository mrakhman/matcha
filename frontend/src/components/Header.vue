<template>
    <div id="header">
        <b-navbar toggleable="lg" variant="light">
            <a href="/"><img alt="Time Club logo" src="../assets/timeclub-logo_orange.png" width="40"></a>
            <h1 class="header_text"> <a href="/"> Matcha </a></h1>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
<!--                    <b-nav-item-dropdown text="My profile" left>-->
<!--                        <b-dropdown-item href="/my_profile">About me</b-dropdown-item>-->
<!--                        <b-dropdown-item href="/my_profile">Settings</b-dropdown-item>-->
<!--                    </b-nav-item-dropdown>-->
<!--                    <b-nav-item href="#">My user</b-nav-item>-->


<!--                    <b-nav-item v-if="session.user_id" to="/my_profile">My profile</b-nav-item>-->
<!--                    What should I put inside ???????? -->
                    <b-nav-item v-bind:to="'/my_profile'">My prof</b-nav-item>
<!--                    <router-link v-bind:to="'my_profile/' + session.user_id"><b-nav-item>My prof</b-nav-item></router-link>-->


                    <b-nav-item href="/users">Users_list</b-nav-item>
                    <b-nav-item href="#" disabled>Disabled</b-nav-item>


<!--                    <b-nav-item v-on:click="auth.loggedIn = !auth.loggedIn">Change AUTH (now it's {{ auth.loggedIn }})</b-nav-item>-->
<!--                    <b-nav-item> AUTH (now it's {{ auth.loggedIn }})</b-nav-item>-->

                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <b-button-group v-if="!session.user_id">
                        <b-button to="/register" variant="outline-primary">Register</b-button>
                        <b-button to="/login" variant="outline-primary">Login</b-button>
                    </b-button-group>

                    <b-nav-item v-if="session.user_id">Hello, {{ session.context.first_name }}!</b-nav-item>
                    <Logout v-if="session.user_id" v-on:del_session="$emit('del_session')"/>

                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>


</template>

<script>
    import Logout from "./Logout";
    import MyProfile from "./MyProfile";

    export default {
        name: "Header.vue",
        components: {
            Logout
        },
        data () {
            return {
                // auth: this.$root.$data.Auth
            }
        },
        props: {
            session: Object
        },
        // computed: {
        //     sessionUser() {
        //         return this.session.user_id;
        //
        //     }
        // }
    }
</script>

<style scoped lang="scss">
    @import '../assets/_custom.scss';
    @import '~bootstrap/scss/bootstrap.scss';
    @import '~bootstrap-vue/src/index.scss';

    #header {
        background-color: #f8f9fa;
        padding: 5px;
    }

    #menu {
        width: 100%;
    }

    .header_text {
        color: black;
        font-size: 24px;
        margin: 5px;
        font-weight: lighter;
    }

    .header_text a {
        color: black;
        text-decoration: none;
    }

    .header_text a:hover {
        color: #396;
    }

    .header_flex_start {
        /*margin-bottom: 10px;*/
        width: 100%;
        text-align: left;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
    }

    .header_flex_end {
        /*text-align: left;*/
        display: flex;
        /*flex-direction: row;*/
        justify-content: flex-end;
    }

    .header_flex_start > img {
        width: 40px;
        height: 40px;
    }


</style>

