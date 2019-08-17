<template>
    <div class="main">
        <h3 class="title"> Notifications </h3>
        <div class="ml-4">
            <b-button class="notif_button" variant="" v-on:click="notifications = notifications2">
                All
            </b-button>
            <b-button class="notif_button" variant="primary" v-on:click="filterByType('message')">
                Messages
            </b-button>
            <b-button class="notif_button" variant="danger" v-on:click="filterByType('like')">
                Likes
            </b-button>
            <b-button class="notif_button" variant="success" v-on:click="filterByType('view')">
                Profile views
            </b-button>
        </div>
        <div class="table">
            <b-row>
                <b-col xl="6">
                    <a class="ml-4" v-if="notifications" href="#" v-on:click="markAllRead">Mark all as read</a>
                    <a class="ml-4" v-else>No unread notifications</a>
                    <b-table striped bordered :items="notifications" :fields="fields">
                        <template slot="N" slot-scope="data">
                            {{ data.index + 1 }}
                        </template>
                        <template slot="created_at" slot-scope="data">
                            {{ data.value }}
                        </template>
                    </b-table>
                </b-col>
            </b-row>
        </div>
    </div>
</template>

<script>
    import {Socket} from "../socket";
    import EventBus from '../event-bus';

    const moment = require('moment');

    export default {
        name: "Notifications.vue",
        data() {
            return {
                fields: [
                    'N',
                    'type',
                    'text',
                    {key: 'created_at', label: 'Date'}
                ],
                notifications: [],
                notifications2: [],
            }
        },
        methods: {
            getNotifications() {
                this.$root.axios.get('/notifications/', {withCredentials: true})
                    .then(response => {
                        this.notifications = response.data["notifications"];

                        this.notifications.forEach(function (message) {
                            message.created_at =  moment.utc(message.created_at).tz("Europe/Paris").format('LLL');
                        });

                        this.notifications2 = this.notifications;
                    })
            },
            markAllRead() {
                this.$root.axios.post('/notifications/all_read', {}, {withCredentials: true})
                    .then(() => {
                        this.getNotifications();
                        EventBus.$emit('markRead');
                    }).catch(() => {});
            },
            filterByType(type) {
                if (this.notifications) {
                    this.notifications = this.notifications2;
                    let notifications = this.notifications;
                    notifications = notifications.filter(notif => notif.type === type);
                    this.notifications = notifications;
                }
            },
            newSocketMsg(data) {
                const payload = JSON.parse(data.data);
                if (payload.type === "notification") {
                    let last_notif = payload.data;
                    last_notif.created_at = moment.utc(last_notif.created_at).tz("Europe/Paris").format('LLL');
                    this.notifications.unshift(last_notif);
                    this.notifications2 = this.notifications;
                }
            }
        },
        created() {
            this.getNotifications();
            Socket.registerHandler(this.newSocketMsg)
        },
        mounted() {
            EventBus.$on('markRead2', () => {
                this.getNotifications();
            });
        }
    }
</script>

<style scoped>
    .notif_button {
        margin: 10px;
    }
    .table {
        margin: 20px;
    }
</style>
