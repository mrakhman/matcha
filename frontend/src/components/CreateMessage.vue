<template>
    <div class="container" style="margin-bottom: 30px">
        <form v-on:submit.prevent="createMessage">
            <input type="text" name="message" class="form-control" placeholder="Enter message..." v-model="new_message">
            <p class="text-danger" v-if="error_text">{{ error_text }}</p>
            <button class="btn btn-primary" type="submit" name="action">Send</button>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "CreateMessage.vue",
        props: ['username'],
        data() {
            return {
                new_message: null,
                error_text: null,

            }
        },
        methods: {
            createMessage() {
                if(this.new_message) {
                    axios.post(this.$root.API_URL + '/chat/send_msg', {
                        text: this.text,
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
                    this.new_message = null;
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

</style>