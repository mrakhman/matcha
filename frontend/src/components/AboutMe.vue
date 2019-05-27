<template>
    <div>
        <pre class="mt-3 mb-0">{{ form }}</pre>
        <pre class="mt-3 mb-0">{{ user_details }}</pre>


        <b-container class="bv-example-row"><b-row><b-col xl="9">



                <h4>Profile main image</h4>
                <b-row id="profile_image_2">
                    <b-col>
                        <b-img class="profile_img" v-bind:src="user_details.profile_image" alt="Profile picture" width="300" rounded></b-img>
                    </b-col>
<!--                    <b-img class="profile_img" v-if="uploaded_image" v-bind:src="uploaded_image" rounded alt="Uploaded image" width="150"></b-img>-->

<!--                    <FileUpload class="m-1" v-model="avatar">-->
                    <b-col>
                        <FileUpload class="m-1">
    <!--                        <div size="150px" v-if="avatar">-->
    <!--                            <img :src="avatar.imageURL" alt="avatar">-->
    <!--                        </div>-->
    <!--                        <div size="150px" v-if="!avatar">-->
    <!--                            <img :src="user_details.profile_image" alt="avatar">-->
    <!--                        </div>-->
                        </FileUpload>
                    </b-col>
                </b-row>

                <br>

                <h4>More photos</h4>
                <b-row id="photos">
                    <b-col>
                        <b-img ref="big_photo" id="big_photo" v-bind:src="photos[0].link" fluid alt="First image" width="300" rounded></b-img>
                        <b-row hei></b-row>
                        <b-row>
                            <img v-on:click="selectPhoto(photo.link)" v-for="photo in photos" v-bind:src="photo.link" alt="image" height="80"/>
                        </b-row>
                    </b-col>
                    <b-col>
                        <FileUpload class="m-1">
                        </FileUpload>
                    </b-col>
                </b-row>

                <br>

            <b-form v-on:submit.prevent="submitAboutMe">
                <b-form-group id="gender_2" label-cols-sm="2" label-cols-lg="2" label="Gender:" label-for="input-horizontal">
                    <b-form-select v-model="user_details.gender" :options="options.gender" size="sm" class="mt-3"></b-form-select>
                    <div class="mt-3">Selected: <strong>{{ user_details.gender }}</strong></div>
                </b-form-group>

                <b-form-group id="sexual_pref_2" label-cols-sm="2" label-cols-lg="2" label="Sexual preferences:" label-for="input-horizontal">
                    <b-form-select v-model="user_details.sex_pref" :options="options.sex_pref" size="sm" class="mt-3"></b-form-select>
                    <div class="mt-3">Selected: <strong>{{ user_details.sex_pref }}</strong></div>
                </b-form-group>
                <b-form-group id="bio_2" label-cols-sm="2" label-cols-lg="2" label="Your biography:" label-for="input-horizontal">
                    <b-form-textarea
                            id="textarea_2"
                            v-model="user_details.bio_text"
                            placeholder="Enter something..."
                            rows="3"
                            max-rows="6"
                    ></b-form-textarea>
                </b-form-group>
                <b-form-group id="tags_2" label-cols-sm="2" label-cols-lg="2" label="Interests:" label-for="input-horizontal">
                    <b-form-group label="What describes you?">
                        <b-form-checkbox-group
                                v-model="user_details.tags"
                                :options="options.tags"
                                name="flavour-1a"
                        ></b-form-checkbox-group>
                    </b-form-group>
                </b-form-group>
                <b-form-group id="birthday_2" label-cols-sm="2" label-cols-lg="2" label="Date of birth:" label-for="input-horizontal" required>
                    <b-form-input v-model="user_details.dob" type="date"></b-form-input> // Date of birth add to user json
                    <div class="mt-3">Age: <strong>{{ user_details.age }}</strong></div>
                    <div class="mt-3">Birthday: <strong>{{ user_details.dob }}</strong></div>
                </b-form-group>

                <b-button type="submit" variant="primary">Save</b-button>
            </b-form>
        </b-col></b-row></b-container>

<br><hr>


        <b-container class="bv-example-row"><b-row><b-col xl="7">
            <div id="profile_image">
                <b-img class="profile_img" src="https://picsum.photos/250/250/?image=54" rounded alt="Profile picture" width="80"></b-img>
                <b-img class="profile_img" src="../assets/timeclub-logo_orange.png" rounded="circle" alt="Profile pic" width="80"></b-img>
            </div>
            <b-form-group id="gender" label-cols-sm="2" label-cols-lg="2" label="Gender:" label-for="input-horizontal">
                <b-form-select v-model="form.gender_selected" :options="options.gender" size="sm" class="mt-3"></b-form-select>
                <div class="mt-3">Selected: <strong>{{ form.gender_selected }}</strong></div>
            </b-form-group>

            <b-form-group id="sexual_pref" label-cols-sm="2" label-cols-lg="2" label="Sexual preferences:" label-for="input-horizontal">
                <b-form-select v-model="form.sexual_selected" :options="options.sex_pref" size="sm" class="mt-3"></b-form-select>
                <div class="mt-3">Selected: <strong>{{ form.sexual_selected }}</strong></div>
            </b-form-group>
            <b-form-group id="bio" label-cols-sm="2" label-cols-lg="2" label="Your biography:" label-for="input-horizontal">
                <b-form-textarea
                        id="textarea"
                        v-model="form.bio_text"
                        placeholder="Enter something..."
                        rows="3"
                        max-rows="6"
                ></b-form-textarea>
            </b-form-group>
            <b-form-group id="tags" label-cols-sm="2" label-cols-lg="2" label="Interests:" label-for="input-horizontal">
                <b-form-group label="What describes you?">
                    <b-form-checkbox-group
                            v-model="form.tags_selected"
                            :options="options.tags"
                            name="flavour-1a"
                    ></b-form-checkbox-group>
                </b-form-group>
            </b-form-group>
            <b-form-group id="birthday" label-cols-sm="2" label-cols-lg="2" label="Date of birth:" label-for="input-horizontal" required>
                <b-form-input v-model="form.dob" type="date"></b-form-input>
            </b-form-group>

            <b-button variant="primary">Save</b-button>

        </b-col></b-row></b-container>

    </div>
</template>

<script>
    import FileUpload from './FileUpload';

    export default {
        name: "AboutMe.vue",
        components: {
            FileUpload
        },
        props: {
            form: Object,
            // options: Object,
            user_details: Object
        },
        data () {
            return {
                // avatar: null,
                options: {
                    gender: [
                        { value: 'female', text: 'Female'},
                        { value: 'male', text: 'Male'},
                        { value: 'not mention', text: 'Not mentioned'}
                    ],
                    sex_pref: ['hetero', 'homo', 'bi'],
                    tags: [
                        { text: '#vegan', value: 'vegan' },
                        { text: '#geek', value: 'geek' },
                        { text: '#tattoos', value: 'tattoos' },
                        { text: '#eco', value: 'eco' }
                    ]
                },
                photos: [
                    {link: require('../../img/qr.png')},
                    {link: require('../../img/face.jpg')},
                    {link: require('../../img/computer.png')},
                    {link: require('../../img/computer.png')},
                    {link: require('../../img/computer.png')}
                ]
            }
        },
        methods: {
            submitAboutMe() {


            },
            selectPhoto(source) {
                this.$refs['big_photo'].src = source
            },
        }
    }
</script>

<style scoped>
    #profile_image {
        padding: 10px;
    }

    .profile_img {
        margin-right: 5px;
    }

</style>
