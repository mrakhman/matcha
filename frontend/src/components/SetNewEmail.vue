<template>
	<div class="main">
		<div v-if="status === true">
			<p> Your email is changed! You can continue using Matcha </p>
		</div>
		<div v-else>
			<p class="text-danger m-3"> Activation link is damaged or has expired </p>
			<p class="m-3"> Go to "My profile -> Settings" to change email again </p>
		</div>
	</div>
</template>

<script>

	export default {
		name: "SetNewEmail.vue",
		data () {
			return {
				status: null,
				token: this.$route.params.token,
			}
		},
		methods: {
			getToken() {
				this.status = null;
				this.$root.axios.get('/settings/activate_email/' + this.token, {withCredentials: true})
					.then(response => {
						if(response.status === 200)
						{
							this.status = true;
							this.$notify({group: 'foo', type: 'success', title: 'Success', text: 'Your email is changed', duration: 3000});
						}
					})
					.catch(() => {
						this.status = false;
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
