<template>
    <div class="main">
        <h3 class="title"> Real time chat </h3>
        <p v-if="messages.length === 0">No messages yet</p>
        <!--    Something for smooth chat scroll    -->
        <div class="messages" v-chat-scroll="{always: false, smooth: true}">
            <div v-for="message in messages" :key="message.id">
<!--                <b-row>-->
                    <b-col v-if="message.sender_id === user.id" xl="2"></b-col>
<!--                    <b-col>-->
                        <span v-if="message.sender_id === user.id" class="text-warning">[me]: </span>

<!--                    </b-col>-->

<!--                </b-row>-->
                <span v-else class="text-info">[{{ message.username }}]: </span>
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
    export default {
        name: "Chat.vue",
        components: {
        },
        props: ['username'],
        data () {
            return {
                id: this.$route.params.id,
                messages: [
                    // {id: null, sender_id: 1, sender_name: 'Masha', time: '3h57m', text: 'blabla'},
                    // {id: null, sender_id: 2, sender_name: 'Dasha', time: '3h57m', text: 'blabla'},
                    // {id: null, sender_id: 2, sender_name: 'Kasha', time: '3h57m', text: 'blabla'},
                ],
                new_message: {sender_id: null, text: null},
                error_text: null,
                user: this.$root.$data.user,
            }
        },
        methods: {
            loadMessages() {axios.get(this.$root.API_URL + '/messages/' + this.id, {withCredentials: true})
                .then(response => {
                    this.messages = response.data.messages;

                    var moment = require('moment');
                    this.messages.forEach(function (message) {
                        message.created_at =  moment.utc(message.created_at).tz("Europe/Paris").format('LLL');
                    });
                    // console.log(response.data.messages);
                })
                // TODO: console
                // eslint-disable-next-line
		            .catch(error => console.log(error));
            },
            addMessage(text) { // also time
                // if(this.new_message.text) {
                                                    // TODO: FROM HERE!!!!!!!!!!
                    this.messages.push({id: null, sender_id: this.user.id, sender_name: this.user.username, created_at: 'time', text: text});
                    // this.new_message.text = null;
                    // this.error_text = null;
                // }
                // else
                    // this.error_text = "No message";
            },
            createMessage() {
                if(this.new_message.text) {
                    axios.post(this.$root.API_URL + '/messages/new', {
                        text: this.new_message.text,
                        receiver_id: this.id
                        // time: Date.now()
                    }, {withCredentials: true})
                        .then(response => {
                            this.addMessage(this.new_message.text); // TODO: FROM HERE!!!!!!!!!!
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
        },
        created() {
			this.loadMessages();
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
