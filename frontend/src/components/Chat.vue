<template>
    <div class="main">
        <h2>RealTime chat</h2>
        <p v-if="messages.length === 0">No messages yet</p>
        <div class="messages" v-chat-scroll="{always: false, smooth: true}">
            <div v-for="message in messages" :key="message.id">
                <span class="text-info">[{{ message.sender_name }}]: </span>
                <span>{{ message.text }}</span>
                <span class="text-secondary time">{{ message.time }}</span>
            </div>
        </div>
        <div class="card-action">
<!--            <CreateMessage v-bind:username="username"/>-->
        </div>
        <b-container fluid>
            <b-row><b-col xl="5">
                <form v-on:submit.prevent="createMessage">
                    <b-form-textarea
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
        </b-container>
    </div>
</template>

<script>
    // import CreateMessage from './CreateMessage';
    import axios from 'axios';
    export default {
        name: "Chat.vue",
        components: {
        },
        props: ['username'],
        data () {
            return {
                chats: [
                    {user_id: 1, username: 'kokoshka', profile_image: require('../../img/qr.png')},
                    {user_id: 2, username: 'Masha', profile_image: require('../../img/face.jpg')},
                    {user_id: 3, username: 'Artemka', profile_image: require('../../img/computer.png')},
                ],
                messages: [
                    {id: null, sender_id: 1, sender_name: 'username', time: '3h57m', text: 'blabla'},
                    {id: null, sender_id: 1, sender_name: 'username', time: '3h57m', text: 'blabla'},
                    {id: null, sender_id: 1, sender_name: 'username', time: '3h57m', text: 'blabla'},
                ],
                new_message: {sender_id: null, chat_id: null, text: null},
                error_text: null,
                // mess: [],
            }
        },
        created() {
            axios.get(this.$root.API_URL + '/chat/dkslkdl', {withCredentials: true})
                .then(response => {
                    // TODO: console
                    console.log(response)
                })
                .catch(error => {
                    // TODO: console
                    console.log(error)
                })
        },
        methods: {
            createMessage() {
                if(this.new_message.text) {
                    axios.post(this.$root.API_URL + '/chat/send_msg', {
                        text: this.new_message.text,
                        username: this.username,
                        time: Date.now()
                    }, {withCredentials: true})
                        .then(response => {
                            // if(response.status === 200)
                            // {
                            //
                            // }
                            // TODO: console
                            console.log(response)
                        })
                        .catch(error => {
                            // TODO: console
                            console.log(error)
                        });
                    this.new_message.text = null;
                    this.error_text = null;
                }
                else {
                    this.error_text = "A message must be entered first";
                }
            }
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
</style>