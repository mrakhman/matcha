<template>
	<div class="main">
		<div v-if="status === true">
			<p> Your account is activated! You can now <router-link v-bind:to="'/login'">login</router-link></p>
		</div>
		<div v-else>
			<p class="text-danger m-3"> Activation link is damaged or has expired </p>
			<br>
			<div class="main"><b-row><b-col xl="5">
				<h4 class=""> Send new link: </h4>
				<p> Enter email you registered your account with </p>
				<form v-on:submit.prevent="resendActivation">
					<b-form-group id="3" label-cols-sm="2" label-cols-lg="2" label="Email" label-for="input-horizontal">
						<b-form-input required v-model="email" type="email"></b-form-input>
						<b-form-text>You will receive new activation link</b-form-text>
					</b-form-group>
					<p class="text-success" v-if="email_sent === true">Check your email!</p>
					<b-button type="submit" variant="primary">Send</b-button>
				</form>
			</b-col></b-row></div>
		</div>
	</div>
</template>

<script>
    import axios from 'axios'

    export default {
		name: "Activation.vue",
		data () {
			return {
				status: null,
				token: this.$route.params.token,
				email: null,
				email_sent: false
			}
		},
		methods: {
			getToken() {
				this.status = null;
				axios.get(this.$root.API_URL + '/settings/activate_user/' + this.token, {withCredentials: true})
					.then(response => {
						if(response.status === 200)
						{
							this.status = true;
							this.$notify({group: 'foo', type: 'success', title: 'Activated!', text: 'Your account is activated, you can now login', duration: -1});
						}
					})
					.catch(() => {
						this.status = false;
					})
			},
			resendActivation() {
				this.email_sent = false;
				axios.post(this.$root.API_URL + '/recovery/resend_activation', {
					email: this.email,
				}, {withCredentials: true})
					.then(response => {
						if(response.status === 200)
						{
							this.$notify({group: 'foo', type: 'success', title: 'Sent', text: 'Activation link is sent to your email', duration: 3000});
							this.email = null;
							this.email_sent = true;
						}
					})
					.catch(error => {
						if (error.response.status === 404) {
							this.$notify({group: 'foo', type: 'error', title: 'Error #404', text: 'User with this email doesn\'t exist', duration: 3000});
						}
					})
			}
		},
		created() {
			this.getToken();
		}
	}
</script>

<style scoped>

</style>
