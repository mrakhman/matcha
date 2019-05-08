<template>
    <div class="main">
        <h3 class="title"> View profile </h3>
<!--        <b-img src="'../../img/' + {{profile.profile_image}}" fluid alt="Profile image"></b-img>-->
        <b-row id="photos">
            <b-col>
                <div class="username"> Username: {{ profile.username }} </div>
                <b-img v-bind:src="profile.profile_image" fluid alt="Profile image" width="450"></b-img>
            </b-col>
            <b-col>
                <b-img ref="big_photo" id="big_photo" v-bind:src="profile.photos[0].link" fluid alt="First image" ></b-img>
                <b-row hei></b-row>
                <b-row>
                    <img v-on:click="selectPhoto(photo.link)" v-for="photo in profile.photos" v-bind:src="photo.link" alt="image" height="100"/>
                </b-row>
            </b-col>
        </b-row>
        <b-row><b-col cols="10">
            <div class="details"> <b> Name: </b> {{profile.first_name}} {{profile.last_name}} </div>
            <div class="details"> <b> Gender: </b> {{profile.gender}} </div>
            <div class="details"> <b> Age: </b> {{profile.age}} </div>
            <div class="details" v-if="sexualPref(profile.sexual_pref, profile.gender)"> <b> I date: </b> {{i_date}} </div>
            <div class="details"><b-col><b-row>
                <b> About me: </b><b-col cols="11">{{profile.bio_text}}</b-col>
            </b-row></b-col></div>
            <div class="details">
                <p class="one_line"><b> I like: </b></p>
                <ul class="tags" v-for="tag in profile.tags">
                    <li> {{tag}} </li>
                </ul>
            </div>
        </b-col></b-row>
        <div class="details">
            <p class="one_line">Did you like my profile?</p>
            <div v-on:click="has_like = !has_like">
                <img v-if="has_like" src="../../img/heart_red.png" width="40">
                <img v-else src="../../img/heart_white.png" width="40">
            </div>
        </div>

    </div>
</template>

<script>
    export default {
        name: "CheckProfile.vue",
        data() {
            return {
                big_photo: '',
                i_date: '',
                has_like: true,
                profile: {
                    first_name: 'Masha',
                    last_name: 'Rakhmasha',
                    username: 'pupok',
                    gender: 'female',
                    age: '23',
                    sexual_pref: 'hetero',
                    bio_text: 'hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka hello, my name is kakashka ',
                    tags: ['hoho', 'haha', 'hihi'],
                    profile_image: require('../../img/face.jpg'),
                    photos: [
                        {link: require('../../img/face.jpg')},
                        {link: require('../../img/qr.png')},
                        {link: require('../../img/computer.png')}
                    ]
                }
            }
        },
        methods: {
            selectPhoto(source) {
                this.$refs['big_photo'].src = source
            },

            sexualPref(my_pref, gender) {
                if (gender === 'female' && my_pref === 'hetero') {
                    return this.i_date = 'boys'
                }
                if (gender === 'male' && my_pref === 'hetero') {
                    return this.i_date = 'girls'
                }
                if (gender === 'male' && my_pref === 'homo') {
                    return this.i_date = 'boys'
                }
                if (gender === 'female' && my_pref === 'homo') {
                    return this.i_date = 'girls'
                }
                if (my_pref === 'bi') {
                    return this.i_date = 'boys and girls'
                }
            }
        },
        mounted() {

        }
    }
</script>

<style scoped>

    #big_photo {
        max-height: 200px;
    }

    .username {
        padding-left: 100px;
    }

    #photos {
        margin: 30px;
    }

    .one_line {
        float: left;
    }

    .tags {
        padding: 0 0 0 8px;
        float: left;
        list-style-type: none;
        /*display: flex;*/
    }

    .details {
        margin-bottom: 5px;
        margin-top: 10px;
    }
</style>
