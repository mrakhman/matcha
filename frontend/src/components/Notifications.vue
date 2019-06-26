<template>
    <div class="main">
        <div class="text-center">
            <b-button class="notif_button" variant="primary">
                Messages
                <b-badge variant="light">9 <span class="sr-only"></span></b-badge>
            </b-button>
            <b-button class="notif_button" variant="danger">
                Likes
                <b-badge variant="light">9 <span class="sr-only"></span></b-badge>
            </b-button>
            <b-button class="notif_button" variant="success">
                Profile views
                <b-badge variant="light">9 <span class="sr-only"></span></b-badge>
            </b-button>
        </div>
        <div class="table">
            <b-row>
                <b-col xl="3"></b-col>
                <b-col xl="5">
                    <a v-if="notifications.length > 0" href="#" v-on:click="markAllRead">Mark all as read</a>
                    <b-table striped bordered :items="notifications" :fields="fields"></b-table>
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
                fields: ['created_at', 'type', 'text'],
                notifications: [
                ]
                // created_at: null, id: null, is_read: null,
            }
        },
        methods: {
            getNotifications() {
                axios.get(this.$root.API_URL + '/notifications/', {withCredentials: true})
                    .then(response => {
                        this.notifications = response.data["notifications"];
                        console.log(response);
                    })
                    // TODO: console
                    // eslint-disable-next-line
                    .catch(error => console.log(error));
            },
            markAllRead() {
                axios.get(this.$root.API_URL + '/notifications/all_read', {withCredentials: true})
                    .then(response => {
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
