<template>
	<div class="main">
		<h3 class="title"> Visit history </h3>
		<div class="table">
			<b-row>
				<b-col md="9">
					<a class="ml-4" v-if="history" href="#" v-on:click="deleteHistory">Delete history</a>
					<a class="ml-4" v-else>No history</a>
					<b-table striped bordered :items="history" :fields="fields">
						<template slot="N" slot-scope="data">
							{{ data.index + 1 }}
						</template>
						<template slot="profile_id" slot-scope="data">
							<router-link v-bind:to="data.value">link</router-link>
						</template>
						<template slot="created_at" slot-scope="data">
							{{ data.value | moment('timezone', "Europe/Paris", 'LLLL') }}
						</template>
					</b-table>
				</b-col>
			</b-row>
		</div>
	</div>
</template>

<script>

	export default {
		name: "History.vue",
		data() {
			return {
				fields: [
					'N',
					'username',
					{
						key: 'profile_id', label: 'Profile',
						formatter: value => {
							return '/users/' + value
						}
					},
					{
						key: 'created_at', label: 'Date',
					}
				],
				history: [],
			}
		},
		methods: {
			getHistory() {
				this.$root.axios.get('/history/', {withCredentials: true})
					.then(response => {
						this.history = response.data["history"];
					}).catch(() => {});
			},
			deleteHistory() {
				this.$root.axios.delete('/history/', {withCredentials: true})
					.then(() => {
						this.getHistory();
					}).catch(() => {});
			}
		},
		created() {
			this.getHistory();

		}
	}
</script>

<style scoped>

</style>
