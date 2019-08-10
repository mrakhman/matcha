<template>
    <div id="header">
        <b-navbar toggleable="lg" variant="light">
            <router-link v-bind:to="'/'"><img alt="Matcha logo" src="../assets/heart_red.png" width="30"></router-link>
            <router-link v-bind:to="'/'"><h1 class="header_text"><a>Matcha</a></h1></router-link>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav v-if="user_id">
                    <b-nav-item v-bind:to="'/my_profile'">My profile</b-nav-item>
                    <b-nav-item v-bind:to="'/search'">Search</b-nav-item>
                    <b-nav-item v-bind:to="'/chat'">Chat</b-nav-item>
                    <b-nav-item v-bind:to="'/notifications'">Notifications</b-nav-item>
                    <b-nav-item v-bind:to="'/history'">History</b-nav-item>
                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <b-button-group v-if="!user_id">
                        <b-button to="/register" variant="outline-primary">Register</b-button>
                        <b-button to="/login" variant="outline-primary">Login</b-button>
                    </b-button-group>

                    <div class="text-center" v-if="user_id">
                        <b-dropdown size="sm" variant="link" toggle-class="text-decoration-none" no-caret right>
                            <template slot="button-content">
                                <b-badge variant="warning" v-if="notifications">{{notifications.length}}</b-badge>
                                <b-badge variant="warning" v-else>0</b-badge>
                                <img alt="Notifications" src="../assets/bell.png" width="30">
                            </template>
                            <b-dropdown-item-button href="#"
                                                    v-if="notifications"
                                                    v-on:click="markAllRead"
                            >Mark all read</b-dropdown-item-button>
                            <b-dropdown-text v-else>No notifications</b-dropdown-text>
                            <b-dropdown-divider></b-dropdown-divider>
                            <div v-for="notification in notifications" v-bind:key="notification.id">
                                <b-dropdown-item v-bind:to="'/notifications'">{{notification.text}}</b-dropdown-item>
                            </div>
                        </b-dropdown>
                    </div>
                    <b-nav-item v-if="user_id">Hello, {{ display_first_name }}!</b-nav-item>
                    <Logout v-if="user_id"/>

                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>


</template>

<script>
    import axios from 'axios'
    import Logout from "./Logout";
    import {Socket} from "../socket";
    import EventBus from '../event-bus';

    export default {
        name: "Header.vue",
        components: {
            Logout
        },
        data () {
            return {
                display_first_name: null,
                user: this.$root.$data.user,
                user_id: this.$root.$data.user_id,

                notifications: []
            }
        },
        methods: {
            getNotifications() {
                axios.get(this.$root.API_URL + '/notifications/', {withCredentials: true})
                    .then(response => {
                        this.notifications = response.data["notifications"];
                    })
                    .catch(() => {});
            },
            getUserFirstName() {
                axios.get(this.$root.API_URL + '/users/me', {withCredentials: true})
                    .then(response => {
                        this.display_first_name = response.data.user.first_name;
                    }).catch(() => {});
            },
            markAllRead() {
                axios.get(this.$root.API_URL + '/notifications/all_read', {withCredentials: true})
                    .then(() => {
                        this.getNotifications();
                        EventBus.$emit('markRead2');
                    }).catch(() => {});
            },
            newSocketMsg(data) {
                const payload = JSON.parse(data.data);
                if (payload.type === "notification") {
                    this.notifications.unshift(payload.data)
                }
            }
        },
        created() {
            this.getNotifications();
            this.getUserFirstName();
            Socket.registerHandler(this.newSocketMsg)
        },
        mounted() {
            EventBus.$on('markRead', () => {
                this.getNotifications();
            });
            EventBus.$on('firstNameChange', (name) => {
                this.display_first_name = name;
            });
        }
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
        width: 100%;
        text-align: left;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
    }

    .header_flex_end {
        display: flex;
        justify-content: flex-end;
    }

    .header_flex_start > img {
        width: 40px;
        height: 40px;
    }


</style>

