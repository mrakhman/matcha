<template>
    <div class="main">
        <div class="ml-4">
<!--            <b-badge variant="light">9 <span class="sr-only"></span></b-badge>-->
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
<!--                <b-col xl="3"></b-col>-->
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
        <pre>{{notifications}}</pre>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Notifications.vue",
        data() {
            return {
                fields: [
                    'N',
                    'type',
                    'text',
                    {key: 'created_at', label: 'Date',
                        formatter: value => {
                            return value.slice(0, 10) + ' at ' + value.slice(11, 16)
                        }
                    }
                ],
                notifications: [],
                notifications2: [],
            }
        },
        methods: {
            getNotifications() {
                axios.get(this.$root.API_URL + '/notifications/', {withCredentials: true})
                    .then(response => {
                        this.notifications = response.data["notifications"];
                        this.notifications2 = this.notifications;
                        console.log(response);
                    })
                    // TODO: console
                    // eslint-disable-next-line
                    .catch(error => console.log(error));
            },
            markAllRead() {
                axios.get(this.$root.API_URL + '/notifications/all_read', {withCredentials: true})
                    .then(response => {
                        this.getNotifications();
                        console.log(response);
                    })
                    // TODO: console
                    // eslint-disable-next-line
                    .catch(error => console.log(error));
            },
            filterByType(type) {
                // this.getNotifications();
                if (this.notifications) {
                    this.notifications = this.notifications2;
                    let notifs = this.notifications;
                    notifs = notifs.filter(notif => notif.type === type);
                    this.notifications = notifs;
                }
            }
        },
        created() {
            this.getNotifications();

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
