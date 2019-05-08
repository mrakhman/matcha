<template>
    <div class="main">
        <h3 class="title"> View profile </h3>
<!--        <b-img src="'../../img/' + {{profile.profile_image}}" fluid alt="Profile image"></b-img>-->
        <b-img v-bind:src="profile.profile_image" fluid alt="Profile image"></b-img>
        <div>
            <b-img v-bind:src="big_photo" fluid alt="Profile image" width="300"></b-img>
            <img v-on:click="" v-for="photo in profile.photos" v-bind:src="photo.link" alt="image" width="100"/>
        </div>
        <div> <b> Name: </b> {{profile.first_name}} {{profile.last_name}} </div>
        <div> <b> Last name: </b>  </div>
    </div>
</template>

<script>
    export default {
        name: "CheckProfile.vue",
        data() {
            return {
                big_photo: '',
                profile: {
                    first_name: 'Masha',
                    last_name: 'Rakhmasha',
                    username: 'pupok',
                    gender: 'female',
                    age: '23',
                    sexual_pref: 'Hetero',
                    bio_text: '',
                    tags: '',
                    profile_image: require('../../img/computer.png'),
                    photos: [
                        {link: require('../../img/face.jpg')},
                        {link: require('../../img/qr.png')},
                        {link: require('../../img/computer.png')}
                    ]
                }
            }
        },

    }
</script>

<style scoped>

</style>
