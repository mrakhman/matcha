<template>
    <div class="main">
        <h3 class="title"> Notifications </h3>
        <div class="ml-4">
            <b-button class="notification_button" variant="" v-on:click="filterByType(null)">
                All
            </b-button>
            <b-button class="notification_button" variant="primary" v-on:click="filterByType('message')">
                Messages
            </b-button>
            <b-button class="notification_button" variant="danger" v-on:click="filterByType('like')">
                Likes
            </b-button>
            <b-button class="notification_button" variant="success" v-on:click="filterByType('view')">
                Profile views
            </b-button>
        </div>
        <div class="table">
            <b-row>
                <b-col md="10">
                    <a class="ml-4" v-if="all_notifications.length" href="#" v-on:click="markAllRead">Delete all notifications</a>
                    <a class="ml-4" v-else>No unread notifications</a>
                    <b-table striped bordered :items="filtered_notifications" :fields="fields">
                        <template slot="N" slot-scope="data">
                            {{ data.index + 1 }}
                        </template>
                        <template slot="created_at" slot-scope="data">
                            {{ data.value | moment('timezone', "Europe/Paris", 'LLLL') }}
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
                filtered_notifications: [],
                all_notifications: [],
                filtered_by: null
            }
        },
        methods: {
            getNotifications() {
                this.$root.axios.get('/notifications/', {withCredentials: true})
                    .then(response => {
                        this.all_notifications = response.data["notifications"];

                        this.filtered_notifications = this.all_notifications;
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
                this.filtered_by = type;
                if (this.filtered_notifications) {
                    if (type != null)
                        this.filtered_notifications = this.all_notifications.filter(n => n.type === type);
                    else
                        this.filtered_notifications = this.all_notifications;
                }
            },
            newSocketMsg(data) {
                const payload = JSON.parse(data.data);
                if (payload.type === "notification") {
                    let last_notification = payload.data;
                    this.all_notifications.unshift(last_notification);
                    this.filterByType(this.filtered_by);
                }
            }
        },
        created() {
            this.getNotifications();
            Socket.registerHandler(this.newSocketMsg, 'notificationsPage')
        },
        mounted() {
            EventBus.$on('markRead2', () => {
                this.getNotifications();
            });
        },
        beforeDestroy() {
            Socket.unregisterHandler('notificationsPage')
        }
    }
</script>

<style scoped>
    .notification_button {
        margin: 10px;
    }
    .table {
        margin: 20px;
    }
</style>
