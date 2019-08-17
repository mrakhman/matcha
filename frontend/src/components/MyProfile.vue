<template>
<div class="main">
    <h3 class="title"> My profile </h3>
    <p v-if="user_details.online" class="text-success ml-3"><b> Online </b></p>
    <p v-else class="text-danger ml-3"><b> Offline <br> <small v-if="user_details.last_connection">Last seen: {{last_online_timezone}}</small></b></p>
    <b-tabs content-class="mt-3">
        <b-tab title="About me" active>
            <AboutMe
                    v-bind:form="form"
                    v-bind:user_details="user_details"
                    v-on:ProfileImageUpdated="getMe"
            />
        </b-tab>

        <b-tab title="Settings">
            <Settings
                    v-bind:form_edit="form_edit"
                    v-bind:alerts="alerts"
                    v-bind:user_details="user_details"
            />
        </b-tab>
    </b-tabs>
</div>
</template>

<script>
    import AboutMe from "./AboutMe";
    import Settings from "./Settings";

    export default {
        name: "MyProfile.vue",
        components: {
            AboutMe,
            Settings
        },
        data() {
            return {
                last_online_timezone: null,
                user_details: {
                    last_connection: ''
                },


                form: {
                    gender_selected: null,
                    sexual_selected: null,
                    tags_selected: [],
                    bio_text: '',
                    dob: ''
                },

                    form_edit: {
                        first_name: '',
                        last_name: '',
                        username: '',
                        email: '',
                        email_password: '',
                        old_password: '',
                        new_password: '',
                    repeat_password: '',
                },

                // options: {
                //     gender: [
                //         { value: 'female', text: 'Female'},
                //         { value: 'male', text: 'Male'},
                //         { value: 'not mention', text: 'Not mentioned'}
                //     ],
                //     sex_pref: ['hetero', 'homo', 'bi'],
                //     tags: [
                //         { text: '#vegan', value: 'vegan' },
                //         { text: '#geek', value: 'geek' },
                //         { text: '#tattoos', value: 'tattoos' },
                //         { text: '#eco', value: 'eco' }
                //     ]
                // },
                alerts: {
                    unauthorized: false,
                    empty_input: false,
                    password_repeat: false,
                    invalid_symbols: false,
                    spaces: false,
                    weak_password: false,
                    wrong_old_password: false,
                    empty_old_password: false,
                    old_new_email_same: false,
                    username_exists: false,
                    email_exists: false,
                    names_saved: false,
                    email_saved: false,
                    password_saved: false,
                },
            }
        },
        methods: {
            getMe() {
                this.$root.axios.get('/users/me', {withCredentials: true})
                    .then(response => {
                        this.user_details = response.data["user"];
                        this.user_details.dob = this.user_details.dob.substring(0, 10);
                    })
                    .catch(() => {});
            },
            editTimezone() {
                const moment = require('moment');
                this.last_online_timezone = moment.tz(this.user_details.last_connection, "Europe/Paris").format('LLL');
            }
        },
        created() {
            this.getMe();
            this.editTimezone();
        },

    }
</script>

<style scoped lang="scss">
    @import '../assets/_custom.scss';
    @import '~bootstrap/scss/bootstrap.scss';
    @import '~bootstrap-vue/src/index.scss';

    #profile_image {
        padding: 10px;
    }

    .profile_img {
        margin-right: 5px;
    }

    .card_section {
        margin-bottom: 20px;
    }

    .title {
        padding-bottom: 20px;
        padding-left: 15px;
    }
</style>



