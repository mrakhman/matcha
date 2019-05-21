<template>
<div class="main">
    <h3 class="title"> My profile </h3>
    <b-alert show variant="danger" dismissible>Username already exists</b-alert>
    <b-alert show variant="danger" dismissible>Another user has this email</b-alert>
    <b-alert show variant="danger" dismissible>Old and new emails are the same</b-alert>
    <b-alert show variant="danger" dismissible>Wrong password</b-alert>
    <b-alert show variant="success" dismissible>Saved!</b-alert>
    <b-alert show variant="success" dismissible>Email will be changed after you confirm it, check your email!</b-alert>
    <b-alert show variant="success" dismissible>Password changed!</b-alert>

    <a href="#">hello</a>


    <b-tabs content-class="mt-3">
        <b-tab title="About me" active>
            <div>
                <b-container class="bv-example-row"><b-row><b-col xl="7">
                    <div id="profile_image">
                        <b-img class="profile_img" src="https://picsum.photos/250/250/?image=54" rounded alt="Profile picture" width="80"></b-img>
                        <b-img class="profile_img" src="../assets/timeclub-logo_orange.png" rounded="circle" alt="Profile pic" width="80"></b-img>
                    </div>
                    <b-form-group id="gender" label-cols-sm="2" label-cols-lg="2" label="Gender:" label-for="input-horizontal">
                        <b-form-select v-model="form.gender_selected" :options="gender" size="sm" class="mt-3"></b-form-select>
                        <div class="mt-3">Selected: <strong>{{ form.gender_selected }}</strong></div>
                    </b-form-group>

                    <b-form-group id="sexual_pref" label-cols-sm="2" label-cols-lg="2" label="Sexual preferences:" label-for="input-horizontal">
                        <b-form-select v-model="form.sexual_selected" :options="sexual_pref" size="sm" class="mt-3"></b-form-select>
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
                                    :options="tags"
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
        </b-tab>



<!--        <b-tab title="Settings" href="#settings" aria-label="Anchor">-->
        <b-tab title="Settings" >
            <div>
                <b-container class="bv-example-row"><b-row><b-col xl="8">
                    <b-alert v-model="errors.empty_input" variant="danger" dismissible>Empty input field</b-alert>
                    <b-alert v-model="errors.password_repeat" variant="danger" dismissible>2 passwords didn't match</b-alert>
                    <b-alert v-model="errors.invalid_symbols" variant="danger" dismissible>Names and email must only include [a-z + A-Z] [0-9] and @</b-alert>
                    <b-alert v-model="errors.spaces" variant="danger" dismissible>Don't use spaces</b-alert>
                    <b-alert v-model="errors.weak_password" variant="danger" dismissible>Password must be 8 chars long, include uppercase, lowercase, number</b-alert>

                    <b-form v-on:submit.prevent="submitChangeNames">
                        <b-card class="card_section" bg-variant="light">
                            <h4 align="center">Name</h4>
                            <b-form-group id="1" label-cols-sm="2" label-cols-lg="2" label="First name" label-for="input-horizontal" required>
                                <b-form-input
                                        v-model="form.first_name"
                                        type="text"
                                ></b-form-input>
                            </b-form-group>

                            <b-form-group id="2" label-cols-sm="2" label-cols-lg="2" label="Last name" label-for="input-horizontal" required>
                                <b-form-input
                                        v-model="form.last_name"
                                        type="text"
                                ></b-form-input>
                            </b-form-group>

                            <b-form-group id="3" label-cols-sm="2" label-cols-lg="2" label="Username" label-for="input-horizontal" required>
                                <b-form-input v-model="form.username" type="text"></b-form-input>
                                <b-form-text>This will be your displayed name</b-form-text>
                            </b-form-group>
                            <b-button type="submit" variant="primary">Save</b-button>
                        </b-card>
                    </b-form>

                    <b-form v-on:submit.prevent="submitChangeEmail">
                        <b-card class="card_section" bg-variant="light">
                            <h4 align="center">Email</h4>
                            <b-form-group id="4" label-cols-sm="2" label-cols-lg="2" label="Email" label-for="input-horizontal" required>
                                <b-form-input v-model="form.email" type="email"></b-form-input>
                                <b-form-text>You will receive email confirmation link</b-form-text>
                            </b-form-group>

                            <b-form-group id="5" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
                                <b-form-input v-model="form.password" type="password"></b-form-input>
                                <b-form-text>Confirm with your password</b-form-text>
                            </b-form-group>
                            <b-button type="submit" variant="primary">Save</b-button>
                        </b-card>
                    </b-form>

                    <b-form v-on:submit.prevent="submitChangePassword">
                        <b-card class="card_section" bg-variant="light">
                            <h4 align="center">Password</h4>
                            <b-form-group id="6" label-cols-sm="2" label-cols-lg="2" label="Old password" label-for="input-horizontal" required>
                            <b-form-input type="password"></b-form-input>
                        </b-form-group>

                            <b-form-group id="7" label-cols-sm="2" label-cols-lg="2" label="New password" label-for="input-horizontal" required>
                                <b-form-input v-model="form.password" type="password" disabled></b-form-input>
                                <b-form-text>Password must be at least 8 chars long, include uppercase, lowercase, symbol, number</b-form-text>
                            </b-form-group>

                            <b-form-group id="8" label-cols-sm="2" label-cols-lg="2" label="Repeat password" label-for="input-horizontal" required>
                                <b-form-input type="password" disabled></b-form-input>
                                <b-form-text>Repeat your new password</b-form-text>
                            </b-form-group>
                            <b-button type="submit" variant="primary">Save</b-button>
                        </b-card>
                    </b-form>

                    <pre class="mt-3 mb-0">{{ form }}</pre>



                </b-col></b-row></b-container>
            </div>
        </b-tab>
        <b-tab title="Disabled" disabled><p>I'm a disabled tab!</p></b-tab>
    </b-tabs>
</div>
</template>

<script>
    export default {
        name: "MyProfile.vue",
        data() {
            return {
                form: {
                    gender_selected: null,
                    sexual_selected: null,
                    tags_selected: [],
                    bio_text: '',
                    birthday: ''
                },

                gender: [
                    { value: 'female', text: 'Female'},
                    { value: 'male', text: 'Male'},
                    { value: 'not mention', text: 'Not mentioned'}
                ],
                // sexual_pref: [
                //     { value: 'straight', text: 'straight'},
                //     { value: 'gay', text: 'gay'},
                //     { value: 'bi-sexual', text: 'bi-sexual'}
                // ]
                sexual_pref: ['hetero', 'homo', 'bi'],
                tags: [
                    { text: '#vegan', value: 'vegan' },
                    { text: '#geek', value: 'geek' },
                    { text: '#tattoos', value: 'tattoos' },
                    { text: '#eco', value: 'eco' }
                ],
                errors: {
                    empty_input: false,
                    password_repeat: false,
                    invalid_symbols: false,
                    spaces: false,
                    weak_password: false
                },
            }
        },
        methods: {
            submitPassword() {
                // Show alert on empty input
                if (!this.form.first_name || !this.form.last_name || !this.form.email || !this.form.username || !this.form.password || !this.form.repeat_password)
                {
                    return this.errors.empty_input = true;
                }

                // Show alert if passwords don't match
                if (this.form.password !== this.form.repeat_password)
                    return this.errors.password_repeat = true;

                // Show alert on space
                if (this.form.first_name.match(/( )/) || this.form.last_name.match(/( )/) || this.form.email.match(/( )/) || this.form.username.match(/( )/) || this.form.password.match(/( )/))
                {
                    return this.errors.spaces = true;
                }

                // Show alert on unwanted characters
                var reg1 = /(?=.*[#$%^&+=§!*?><(){[\]}'";:~])/;
                if (this.form.first_name.match(reg1) || this.form.last_name.match(reg1) || this.form.email.match(reg1) || this.form.username.match(reg1))
                {
                    return this.errors.invalid_symbols = true;
                }

                // Uncomment me later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                // // Show alert on weak password
                // var reg2 = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
                // if (!this.form.password.match(reg2))
                // {
                //     return this.errors.weak_password = true;
                // }

                else
                    alert((JSON.stringify(this.form)))
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
</style>
