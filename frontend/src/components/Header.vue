<template>
    <div id="header">
        <b-navbar toggleable="lg" variant="light">
            <router-link v-bind:to="'/'"><img alt="Matcha logo" src="../../img/heart_red.png" width="30"></router-link>
            <router-link v-bind:to="'/'"><h1 class="header_text"><a>Matcha</a></h1></router-link>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav v-if="user_id">
<!--                    <b-nav-item-dropdown text="My profile" left>-->
<!--                        <b-dropdown-item v-bind:to="'/my_profile/about_me'">About me</b-dropdown-item>-->
<!--                        <b-dropdown-item v-bind:to="'/my_profile/settings'">Settings</b-dropdown-item>-->
<!--                    </b-nav-item-dropdown>-->
<!--                    <b-nav-item href="#">My user</b-nav-item>-->


<!--                    <b-nav-item v-if="session.user_id" to="/my_profile">My profile</b-nav-item>-->
<!--                    What should I put inside ???????? -->
                    <b-nav-item v-bind:to="'/my_profile'">My profile</b-nav-item>
<!--                    <router-link v-bind:to="'my_profile/' + session.user_id"><b-nav-item>My prof</b-nav-item></router-link>-->


                    <b-nav-item v-bind:to="'/search'">Search</b-nav-item>
                    <b-nav-item v-bind:to="'/notifications'">Notifs</b-nav-item>
                    <b-nav-item v-bind:to="'/chat'">Chat</b-nav-item>
<!--                    <b-nav-item href="#" disabled>Disabled</b-nav-item>-->


<!--                    <b-nav-item v-on:click="auth.loggedIn = !auth.loggedIn">Change AUTH (now it's {{ auth.loggedIn }})</b-nav-item>-->
<!--                    <b-nav-item> AUTH (now it's {{ user_id }})</b-nav-item>-->

                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <b-button-group v-if="!user_id">
                        <b-button to="/register" variant="outline-primary">Register</b-button>
                        <b-button to="/login" variant="outline-primary">Login</b-button>
                    </b-button-group>

                    <div class="text-center" v-if="user_id">
                        <b-dropdown size="sm" variant="link" toggle-class="text-decoration-none" no-caret>
                            <template slot="button-content">
                                <b-badge variant="warning" v-if="notifs">{{notifs.length}}</b-badge>
                                <b-badge variant="warning" v-else>0</b-badge>
                                <img alt="Notifications" src="../../img/bell.png" width="30">
                            </template>
                            <div v-for="notif in notifs" v-bind:key="notif.id">
                                <b-dropdown-item v-bind:to="'/notifications'">{{notif.text}}</b-dropdown-item>
                            </div>
                        </b-dropdown>
                    </div>
                    <b-nav-item v-if="user_id">Hello, {{ user.first_name }}!</b-nav-item>
                    <Logout v-if="user_id"/>
<!--                    v-on:del_session="$emit('del_session')"/>-->

                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>


</template>

<script>
    import axios from 'axios'
    import Logout from "./Logout";
    import Notifications from "./Notifications";
    // import MyProfile from "./MyProfile";

    export default {
        name: "Header.vue",
        components: {
            Logout,
            Notifications
        },
        data () {
            return {
                user: this.$root.$data.user,
                user_id: this.$root.$data.user_id,

                notifs: [
                    // { id: 4, type: 'message', text: 'you received a new message' },
                    // { id: 3, type: 'like', text: 'XX liked you' },
                    // { id: 2, type: 'view', text: 'ZZ checked your profile' },
                    // { id: 1, type: 'message', text: 'Carney replied' }
                ]
            }
        },
        props: {
            // session: Object
        },
        methods: {
            getNotifications() {
                axios.get(this.$root.API_URL + '/notifications/', {withCredentials: true})
                    .then(response => {
                        this.notifs = response.data["notifications"];
                        console.log(response);
                    })
                    // TODO: console
                    // eslint-disable-next-line
                    .catch(error => console.log(error));
            }
        },
        created() {
            this.getNotifications();
        }

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
        text-decoration: none;
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

