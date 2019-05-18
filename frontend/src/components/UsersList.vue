<template>
    <div class="main">
        <h3> Users List </h3>
        <b-row>
            <div v-for="user in users" :key="user.id">
                <b-card v-bind:title="user.first_name + ' ' + user.last_name"
                        v-bind:img-src="user.profile_image"
                        img-alt="profile picture"
                        style="max-width: 15rem;"
                        class="mb-2 add_space"
                >
                    <b-card-text>
                        {{user.age}} <br>
                        {{user.gender}} <br>
                        {{user.tags}} <br>
                        {{user.sex_pref}}
                    </b-card-text>

                    <b-button href="#" variant="primary">Open</b-button>
                </b-card>
            </div>

<!--            <b-card v-bind:title="user.first_name + ' ' + user.last_name"-->
<!--                    v-bind:img-src="photos[1].link"-->
<!--                    img-alt="profile picture"-->
<!--                    style="max-width: 15rem;"-->
<!--                    class="mb-2 add_space"-->
<!--            >-->
<!--                <b-card-text>-->
<!--                    {{user.age}} <br>-->
<!--                    {{user.gender}} <br>-->
<!--                    {{user.tags}} <br>-->
<!--                    {{user.sex_pref}}-->
<!--                </b-card-text>-->

<!--                <b-button href="#" variant="primary">Open</b-button>-->
<!--            </b-card>-->
        </b-row>
        <div>

        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "UsersList.vue",

    data() {
        return {
            users: [],
            profile_image: require('../../img/face.jpg'),
            photos: [
                {link: require('../../img/face.jpg')},
                {link: require('../../img/qr.png')},
                {link: require('../../img/computer.png')}
            ]

        }
    },

    methods: {

    },

    created() {
        axios.get('http://localhost:5000/users/page/1')
            .then(res => this.users = res.data["users"])
            .then(res => console.log(res))
            .catch(err => console.log(err));
    }
}
</script>

<style scoped>
    .add_space {
        margin: 10px;
    }

</style>
