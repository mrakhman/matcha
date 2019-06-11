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
                <b-table striped bordered :items="items"></b-table>
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
                    { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                    { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                    { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                    { age: 38, first_name: 'Jami', last_name: 'Carney' }
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
