<template>
<div>
    <h3>My profile</h3>
    <b-tabs content-class="mt-3">
        <b-tab title="About me" active>
            <div>
                <b-container class="bv-example-row"><b-row><b-col xl="9">
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
                        <p>#hehe #hihi #haha</p>
                    </b-form-group>
                    <b-form-group id="birthday" label-cols-sm="2" label-cols-lg="2" label="Date of birth:" label-for="input-horizontal" required>
                        <b-form-input v-model="form.birthday" type="date"></b-form-input>
                    </b-form-group>

                    <b-button variant="primary">Save</b-button>
                    <pre class="mt-3 mb-0">{{ form }}</pre>
                </b-col></b-row></b-container>
            </div>
        </b-tab>



        <b-tab title="Settings"><p>I'm the second tab</p></b-tab>
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
                    food: null,
                    gender_selected: null,
                    sexual_selected: null,
                    bio_text: '',
                    birthday: '12/01/1995'
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
                sexual_pref: ['straight', 'gay', 'bi-sexual'],

            }
        }
    }
</script>

<style scoped>

</style>
