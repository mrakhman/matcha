<template>
    <div>
        <pre class="mt-3 mb-0">{{ form }}</pre>
        <pre class="mt-3 mb-0">{{ user_details }}</pre>


        <b-container class="bv-example-row"><b-row><b-col xl="7">
            <div id="profile_image_2">
                <b-img class="profile_img" v-bind:src="user_details.profile_image" rounded alt="Profile picture" width="100"></b-img>
            </div>
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
                <b-form-input v-model="form.dob" type="date"></b-form-input> // Date of birth add to user json
                <div class="mt-3">Age: <strong>{{ user_details.age }}</strong></div>
            </b-form-group>

            <b-button variant="primary">Save</b-button>
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
    export default {
        name: "AboutMe.vue",
        props: {
            form: Object,
            // options: Object,
            user_details: Object
        },
        data () {
            return {
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
            }
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
