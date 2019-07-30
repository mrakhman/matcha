<template>
    <div>
        <br><hr>
        <b-container>
            <b-row><b-col xl="6">
                <b-row class="message_block p-2 mb-3" v-for="user in users_list" :key="user.id" align-v="center">
                    <b-col>
                        <b-img v-if="user.profile_image" v-bind="image_style" :src="user.profile_image" rounded="circle" alt="Circle image"></b-img>
                        <b-img v-else v-bind="no_image" rounded="circle" alt="Circle image"></b-img>
                    </b-col>
                    <b-col>
                        <h4>{{user.username}}</h4>
                    </b-col>
                    <b-col>
                        <router-link v-bind:to="'chat/' + user.id">
                            <b-button variant="outline-secondary">Open chat</b-button>
                        </router-link>
                    </b-col>
                </b-row>

            </b-col></b-row>
        </b-container>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "CreateMessage.vue",
        props: ['username'],
        data() {
            return {
                users_list: [],
                image_style: {width: 75, height: 75, class: 'm1'},
                no_image: {blank: true, blankColor: '#777', width: 75, height: 75, class: 'm1'}
            }
        },
        methods: {
            getChatList() {
                axios.get(this.$root.API_URL + '/messages/chats', {withCredentials: true})
                .then(response => {
                    this.users_list = response.data.chats;
                    // console.log(response.data);
                })
                    // TODO: console
                    // eslint-disable-next-line
		            .catch(error => console.log(error));
            }
        },
        created() {
            this.getChatList();
       }
    }
</script>

<style scoped>
    .message_block {
        background-color: #f8f9fa;
        border-radius: 7px;
    }

</style>
