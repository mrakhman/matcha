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
            <b-row><b-col xl="9">
                <b-table striped bordered v-bind:items="items"></b-table>
            </b-col></b-row>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Notifications.vue",
        data() {
            return {
                items: [
                    { id: 4, type: 'message', text: 'you received a new message' },
                    { id: 3, type: 'like', text: 'XX liked you' },
                    { id: 2, type: 'view', text: 'ZZ checked your profile' },
                    { id: 1, type: 'message', text: 'Carney replied' }
                ]
            }
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
