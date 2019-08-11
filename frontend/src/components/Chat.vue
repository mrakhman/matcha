<template>
    <div class="main">
        <h3 class="title"> Real time chat </h3>
        <p v-if="messages.length === 0">No messages yet</p>
        <!--    Something for smooth chat scroll    -->
        <div class="messages" v-chat-scroll="{always: false, smooth: true}">
            <div v-for="message in messages" :key="message.id">
                <b-col v-if="message.sender_id === user.id" xl="2"></b-col>
                <span v-if="message.sender_id === user.id" class="text-warning">[me]: </span>
                <span v-else class="text-info">[{{ chat_users[message.sender_id].username }}]: </span>
                <span>{{ message.text }}</span>
                <span class="text-secondary time">{{ message.created_at }}</span>
            </div>
        </div>
        <b-row><b-col xl="5">
            <form v-on:submit.prevent="createMessage">
                <b-form-textarea
                    class="mt-3 mb-3"
                    id="textarea"
                    v-model="new_message.text"
                    placeholder="Enter message..."
                    rows="2"
                    max-rows="6"
                ></b-form-textarea>
                <p class="text-danger" v-if="error_text">{{ error_text }}</p>
                <b-button type="submit" variant="outline-primary">Send</b-button>
            </form>
        </b-col></b-row>
    </div>
</template>

<script>
    import axios from 'axios';
    import {Socket} from "../socket";

    const moment = require('moment');
    export default {
        name: "Chat.vue",
        components: {
        },
        props: ['username'],
        data () {
            return {
                id: this.$route.params.id,
                messages: [],
                new_message: {sender_id: null, text: null},
                error_text: null,
                user: this.$root.$data.user,
                chat_users: [],
            }
        },
        methods: {
            loadMessages() {axios.get(this.$root.API_URL + '/messages/' + this.id, {withCredentials: true})
                .then(response => {
                    this.messages = response.data.messages;
                    this.chat_users = response.data.users;

                    this.messages.forEach(function (message) {
                        message.created_at =  moment.utc(message.created_at).tz("Europe/Paris").format('LLL');
                    });
                })
            },
            createMessage() {
                if(this.new_message.text) {
                    axios.post(this.$root.API_URL + '/messages', {
                        text: this.new_message.text,
                        receiver_id: this.id
                    }, {withCredentials: true})
                        .catch(() => {
                            this.error_text = "Two users are blocked or not connected, you can't chat";
                        });
                    this.new_message.text = null;
                    this.error_text = null;
                }
                else {
                    this.error_text = "A message must be entered first";
                }
            },
            newSocketMsg(data) {
                const payload = JSON.parse(data.data);
                if (payload.type === "message") {
                    payload.data.created_at =  moment.utc(payload.data.created_at).tz("Europe/Paris").format('LLL');
                    this.messages.push(payload.data)
                }
            }
        },
        created() {
			this.loadMessages();
            Socket.registerHandler(this.newSocketMsg);
        },
        mounted() {
            setTimeout(() => this.$socket.sendObj({"action": "open_chat", "companion_id": this.id}), 4000);
        },
        beforeDestroy() {
            this.$socket.sendObj({"action": "close_chat"});
        }
    }
</script>

<style scoped>
    .chat h2 {
        font-size: 2.6em;
        margin-bottom: 0;
    }
    .chat h5 {
        margin-top: 0;
        margin-bottom: 40px;
    }

    .chat span {
        font-size: 1.2em;
    }

    .time {
        display: block;
        font-size: 0.7em;
    }

    .messages {
        max-height: 300px;
        overflow: auto;
    }
    .my_message {
        float: right;
    }
</style>
