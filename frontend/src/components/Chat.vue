<template>
    <div class="main">
        <h3 class="title"> Real time chat </h3>
        <p v-if="messages.length === 0">No messages yet</p>
        <!--    Something for smooth chat scroll    -->
        <div class="messages" v-chat-scroll="{always: false, smooth: true}">
            <div v-for="message in messages" :key="message.id">
                <div class="m-3">
                    <span class="text-secondary time">{{ message.created_at | moment('timezone', "Europe/Paris", 'LLLL') }}</span>
                    <span v-if="message.sender_id === user.id" class="text-warning">
                        <b-img
                                v-if="chat_users[message.sender_id].profile_image"
                                v-bind="image_style"
                                :src="chat_users[user.id].profile_image"
                                rounded="circle"
                                alt="Circle image">
                        </b-img>
                        <b-img
                            v-else
                            v-bind="no_image"
                            rounded="circle"
                            alt="Circle image">
                        </b-img>
                        [me]:
                    </span>
                    <span v-else>
                        <router-link class="profile-link text-info" v-bind:to="'/users/' + id">
                            <b-img
                                    v-if="chat_users[message.sender_id].profile_image"
                                    v-bind="image_style"
                                    :src="chat_users[message.sender_id].profile_image"
                                    rounded="circle"
                                    alt="Circle image">
                            </b-img>
                            <b-img
                                    v-else
                                    v-bind="no_image"
                                    rounded="circle"
                                    alt="Circle image">
                            </b-img>
                            [{{ chat_users[message.sender_id].username }}]:
                        </router-link>
                    </span>
                    <span>{{ message.text }}</span>
                </div>
            </div>
        </div>
        <b-row><b-col md="6">
            <form v-on:submit.prevent="createMessage">
                <b-form-textarea
                    class="mt-3 mb-3"
                    id="textarea"
                    v-model="new_message.text"
                    v-if="users_can_chat"
                    placeholder="Enter message..."
                    rows="2"
                    max-rows="6"
                ></b-form-textarea>
                <p class="text-danger" v-if="error_text">{{ error_text }}</p>
                <b-button type="submit" variant="outline-primary" v-if="users_can_chat">Send</b-button>
                <p class="text-danger mt-3" v-else>One of you are blocked or disliked another one, you can't chat</p>
            </form>
        </b-col></b-row>
    </div>
</template>

<script>
    import {Socket} from "../socket";
    import {mapState} from 'vuex';

    export default {
        name: "Chat.vue",
        props: ['username'],
        data () {
            return {
                image_style: {width: 35, height: 35, class: 'm-1'},
                no_image: {blank: true, blankColor: '#777', width: 35, height: 35, class: 'm-1'},
                id: this.$route.params.id,
                messages: [],
                new_message: {sender_id: null, text: null},
                error_text: null,
                chat_users: [],
                users_can_chat: null
            }
        },
        computed: mapState(['user']),
        methods: {
            loadMessages() {
                this.$root.axios.get('/messages/' + this.id, {withCredentials: true})
                .then(response => {
                    this.messages = response.data.messages;
                    this.chat_users = response.data.users;
                })
            },
            usersCanChat() {
                this.$root.axios.get('/messages/'+ this.id + '/allowed', {
                    withCredentials: true
                })
                        .then(response => {
                            if (response.status === 200 && response.data.ok === true)
                                this.users_can_chat = true;
                            else if (response.status === 200 && response.data.ok === false)
                                this.users_can_chat = false;
                        }).catch(() => {});
            },
            createMessage() {
                if(this.new_message.text) {
                    this.$root.axios.post('/messages', {
                        text: this.new_message.text,
                        receiver_id: this.id
                    }, {withCredentials: true})
                        .catch(() => {
                            this.error_text = "One of you are blocked or disliked another one, you can't chat";
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
                    this.messages.push(payload.data)
                }
            }
        },
        created() {
			this.loadMessages();
			this.usersCanChat();
            Socket.registerHandler(this.newSocketMsg, 'chat');
        },
        mounted() {
            setTimeout(() => this.$socket.sendObj({"action": "open_chat", "companion_id": this.id}), 4000);
        },
        beforeDestroy() {
            this.$socket.sendObj({"action": "close_chat"});
            Socket.unregisterHandler('chat');
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
        max-height: 600px;
        overflow: auto;
    }
    .profile-link {
        text-decoration: none;
    }
</style>
