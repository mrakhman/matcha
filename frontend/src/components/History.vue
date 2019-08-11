<template>
	<div class="main">
		<h3 class="title"> Visit history </h3>
		<div class="table">
			<b-row>
				<b-col xl="6">
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
							{{ data.value }}
						</template>
					</b-table>
				</b-col>
			</b-row>
		</div>
	</div>
</template>

<script>
    import axios from 'axios';

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
				axios.get(this.$root.API_URL + '/history', {withCredentials: true})
					.then(response => {
						this.history = response.data["history"];

						let moment = require('moment');
						this.history.forEach(function (message) {
							message.created_at = moment.utc(message.created_at).tz("Europe/Paris").format('LLL');
						});
					}).catch(() => {});
			},
			deleteHistory() {
				axios.delete(this.$root.API_URL + '/history', {withCredentials: true})
					.then(() => {
						this.getHistory();
						this.$router.go(0);
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
