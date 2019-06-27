<template>
<div class="main">
    <h3 class="title"> My profile </h3>

    <b-tabs content-class="mt-3">
        <b-tab title="About me" active>
            <AboutMe
                    v-bind:form="form"
                    v-bind:user_details="user_details"
                    v-on:ProfileImageUpdated="getMe"
            />
        </b-tab>

<!--        <b-tab title="Settings" href="#settings" aria-label="Anchor">-->
        <b-tab title="Settings">
            <Settings
                    v-bind:form_edit="form_edit"
                    v-bind:alerts="alerts"
                    v-bind:user_details="user_details"
            />
        </b-tab>
<!--        <b-tab title="Disabled" disabled><p>I'm a disabled tab!</p></b-tab>-->
    </b-tabs>
</div>
</template>

<script>
    import AboutMe from "./AboutMe";
    import Settings from "./Settings";
    import axios from 'axios';

    export default {
        name: "MyProfile.vue",
        components: {
            AboutMe,
            Settings
        },
        // props: ['user_id'],
        data() {
            return {

                // user_id: this.$props.user_id,
                user_details: {},


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
        created() {
            this.getMe();
        },
        methods: {
            getMe() {
                axios.get(this.$root.API_URL + '/users/me', {withCredentials: true})
                    .then(response => {
                        this.user_details = response.data["user"];
                        this.user_details.dob = this.user_details.dob.substring(0, 10);
                        // return response // IDK why I need it???
                    })
                    // TODO: console
                    // eslint-disable-next-line
                    .catch(error => console.log(error));
            }
        }

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

    /*v-bind:options="options"*/
</style>



