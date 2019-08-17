<template>
	<div class="main">
		<div v-if="status === true">
			<p> You can reset your password:</p>
			<div class="main"><b-row><b-col xl="5">
				<form v-on:submit.prevent="resetPassword">
					<b-form-group id="5" label-cols-sm="2" label-cols-lg="2" label="Password" label-for="input-horizontal" required>
						<b-form-input required v-model="password" type="password"></b-form-input>
						<b-form-text>Password must be at least 8 chars long, include uppercase, lowercase, number</b-form-text>
					</b-form-group>
					<b-form-group id="6" label-cols-sm="2" label-cols-lg="2" label="Repeat password" label-for="input-horizontal" required>
						<b-form-input required v-model="repeat_password" type="password"></b-form-input>
						<b-form-text>Repeat your password</b-form-text>
					</b-form-group>
					<p class="text-success" v-if="reset_success === true">Password reset! <router-link v-bind:to="'/login'">Login</router-link> with your new password</p>
					<b-button type="submit" variant="primary">Save</b-button>
				</form>
			</b-col></b-row></div>
		</div>
		<div v-else>
			<p class="text-danger"> Password reset link is damaged or has expired </p>
			<router-link v-bind:to="'/forgot_password'"> Reset password again </router-link>
		</div>
	</div>
</template>

<script>

	export default {
		name: "ResetPassword.vue",
		data () {
			return {
				status: null,
				token: this.$route.params.token,
				password: null,
				repeat_password: null,
				reset_success: false
			}
		},
		methods: {
			getResetToken() {
				this.status = null;
				this.$root.axios.get('/recovery/reset_password/' + this.token, {withCredentials: true})
					.then(response => {
						if(response.status === 200)
						{
							this.status = true;
						}
					})
					.catch(() => {
						this.status = false;
					})
			},
			validateFields() {
				let has_error = 0;

				// Show alert on empty input
				if (!this.password || !this.repeat_password)
				{
					this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Empty input field', duration: 3000});
					has_error = 1;
				}

				// Show alert if passwords don't match
				if (this.password !== this.repeat_password) {
					this.$notify({group: 'foo', type: 'error', title: 'Error', text: '2 passwords didn\'t match', duration: 3000});
					has_error = 1;
				}

				// Show alert on space
				if (this.password.match(/( )/))
				{
					this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Don\'t use spaces', duration: 3000});
					has_error = 1;
				}

				// Show alert on weak password
				const reg2 = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
				if (!this.password.match(reg2))
				{
					this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Weak password: password must be at least 8 chars long, include uppercase, lowercase, number and no symbols', duration: -1});
					has_error = 1;
				}

				return has_error === 1;

			},
			resetPassword() {
				this.reset_success = false;
				if (this.validateFields())
					return false;

				this.$root.axios.post('/users/reset_password/' + this.token, {
					password: this.password,
				}, {withCredentials: true})
					.then(response => {
						if(response.status === 200)
						{
							this.reset_success = true;
							this.$notify({group: 'foo', type: 'success', title: 'Saved!', text: 'Password reset, you can now login!', duration: 3000});
							this.password = null;
							this.repeat_password = null;
						}
					})
					.catch(() => {})
			}
		},
		created() {
			this.getResetToken();
		}
	}
</script>

<style scoped>

</style>
