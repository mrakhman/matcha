<template>
    <div class="main">
        <h3> Users List </h3>
        <b-row>
            <b-card v-bind:title="user.first_name + ' ' + user.last_name"
                    v-bind:img-src="profile_image"
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

            <b-card v-bind:title="user.first_name + ' ' + user.last_name"
                    v-bind:img-src="photos[1].link"
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
            user: [],
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
        axios.get('http://localhost:5000/users/1')
            .then(res => this.user = res.data)
            .catch(err => console.log(err));
    }
}
</script>

<style scoped>
    .add_space {
        margin: 10px;
    }

</style>
