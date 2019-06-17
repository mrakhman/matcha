<template>
    <div>
        <pre class="mt-3 mb-0">{{ user_details }}</pre>

        <b-container class="bv-example-row"><b-row><b-col xl="9">

                <h4>Profile main image</h4>
                <b-row id="profile_image_2">
                    <b-col>
                        <b-img class="profile_img" v-if="user_details.profile_image" v-bind:src="user_details.profile_image" alt="Profile picture" width="300" rounded></b-img>
                    </b-col>
                    <b-col>
                        <FileUpload
                                class="m-1"
                                uploadFieldName="profile_image"
                                :max="1"
                                :many="false"
                                v-bind:images="user_details.profile_image"
                                v-on:ImageUploadSuccess="() => {this.$emit('ProfileImageUpdated')}"
                        ></FileUpload>
                    </b-col>
                </b-row>

                <br>

                <h4>More images</h4>
                <b-row id="photos">
                    <b-col>
                        <b-img v-if="images.length > 0" ref="big_photo" v-bind:id="images[0].id" v-bind:src="images[0].src" fluid alt="First image" width="300" rounded></b-img>
                        <b-row>

                        </b-row>
                        <b-button class="mt-1 mb-3" type="" variant="danger" size="sm" v-if="images.length > 0" v-on:click="deleteImage">Delete</b-button>
                        <b-row v-if="images.length > 0">
                            <img alt="image" height="80"
                                    v-on:click="selectPhoto(image.src, image.id)"
                                    v-for="image in images"
                                    v-bind:src="image.src"
                                    v-bind:key="image.id"
                            />
                        </b-row>
                    </b-col>
                    <b-col>
                        <FileUpload class="m-1"
                                    uploadFieldName="user_image"
                                    :max="5"
                                    :many="true"
                                    v-bind:images="images"
                                    v-on:ImageUploadSuccess="updateImageList"
                        ></FileUpload>
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
<!--                    <div class="mt-3">Age: <strong>{{ user_details.age }}</strong></div>-->
                    <div class="mt-3">Birthday: <strong>{{ user_details.dob }}</strong></div>
                </b-form-group>

                <b-button type="submit" variant="primary">Save</b-button>
                <p class="text-success" v-if="edit_success_alert">saved!</p>
            </b-form>
        </b-col></b-row></b-container>

<br><hr>

    </div>
</template>

<script>
    import FileUpload from './FileUpload';
    import axios from 'axios';

    export default {
        name: "AboutMe.vue",
        components: {
            FileUpload
        },
        props: {
            form: Object,
            user_details: Object
        },
        data () {
            return {
                edit_success_alert: false,
                options: {
                    gender: [
                        { value: 'female', text: 'Female'},
                        { value: 'male', text: 'Male'},
                        // { value: 'not mention', text: 'Not mentioned'}
                    ],
                    sex_pref: ['hetero', 'homo', 'bi'],
                    tags: ['eco', 'geek', 'veggie', 'travel', '42', 'music'],
                },
                images: [
                    {id: null, src: null}
                ]
            }
        },
        methods: {
            submitAboutMe() {
                axios.post(this.$root.API_URL + '/users/edit_profile', {
                    gender: this.user_details.gender,
                    sex_pref: this.user_details.sex_pref,
                    bio_text: this.user_details.bio_text,
                    profile_image: this.user_details.profile_image,
                    dob: this.user_details.dob,
                    // images:
                    // tags:
                }, {withCredentials: true})
                    .then(response => {
                        if(response.status === 200)
                        {
                            this.edit_success_alert = true;
                            this.$notify({group: 'foo', type: 'success', title: 'Saved!', text: 'personal details are updated', duration: -1})
                        }
                        // TODO: console
                        console.log(response)
                    })
                    .catch(error => {
                        // TODO: console
                        console.log(error)
                    })

            },
            selectPhoto(src, id) {
                this.$refs['big_photo'].src = src;
                this.$refs['big_photo'].id = id;
            },
            deleteImage() {
                if (confirm("Delete image?")) {
                    var del_img_id = this.$refs['big_photo'].id;

                    axios.delete(this.$root.API_URL + '/images/' + del_img_id,
                        {
                            withCredentials: true
                        })
                        .then(response => {
                            if(response.status === 200)
                            {
                                this.$notify({group: 'foo', type: 'success', title: 'Deleted', text: 'Image deleted', duration: -1});
                                this.updateImageList();
                                console.log(response)
                            }
                        })
                        // TODO: console
                        // eslint-disable-next-line
                        .catch(error => {
                            console.log(error)
                        })
                }
            },
            updateImageList() {
                axios.get(this.$root.API_URL + '/users/' + this.$root.$data.user_id, {
                    params: {with_images: true},
                    withCredentials: true
                })
                    .then(response => {
                        this.images = response.data.user.images;
                        // console.log(response.data.user);
                    })
                    // TODO: console
                    // eslint-disable-next-line
                    .catch(error => console.log(error));
            }
        },
        created() {
            this.updateImageList();

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
