<template>
    <div>
        <b-container class="bv-example-row"><b-row><b-col xl="7">
            <div id="profile_image">
                <b-img class="profile_img" src="https://picsum.photos/250/250/?image=54" rounded alt="Profile picture" width="80"></b-img>
                <b-img class="profile_img" src="../assets/timeclub-logo_orange.png" rounded="circle" alt="Profile pic" width="80"></b-img>
            </div>
            <b-form-group id="gender" label-cols-sm="2" label-cols-lg="2" label="Gender:" label-for="input-horizontal">
                <b-form-select v-model="form.gender_selected" :options="user.gender" size="sm" class="mt-3"></b-form-select>
                <div class="mt-3">Selected: <strong>{{ form.gender_selected }}</strong></div>
            </b-form-group>

            <b-form-group id="sexual_pref" label-cols-sm="2" label-cols-lg="2" label="Sexual preferences:" label-for="input-horizontal">
                <b-form-select v-model="form.sexual_selected" :options="user.sexual_pref" size="sm" class="mt-3"></b-form-select>
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
                            :options="user.tags"
                            name="flavour-1a"
                    ></b-form-checkbox-group>
                </b-form-group>
            </b-form-group>
            <b-form-group id="birthday" label-cols-sm="2" label-cols-lg="2" label="Date of birth:" label-for="input-horizontal" required>
                <b-form-input v-model="form.birthday" type="date"></b-form-input>
            </b-form-group>

            <b-button variant="primary">Save</b-button>
            <pre class="mt-3 mb-0">{{ form }}</pre>
        </b-col></b-row></b-container>
    </div>
</template>

<script>
    export default {
        name: "AboutMe.vue",
        props: {
            form: Object,
            user: Object
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
