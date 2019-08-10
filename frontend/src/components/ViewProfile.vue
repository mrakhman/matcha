<template>
	<div class="main">
		<div id="user_not_exist" v-if="user_not_exist">
			<h3>No user</h3>
			<p>Sorry, this user doesn't exist</p>
		</div>
		<div id="user_exists" v-else>
			<h3 class="title"> View profile: <b>{{ user.username }}</b> </h3>
			<p v-if="user.online" class="text-success ml-3"><b> Online </b></p>
			<p v-else class="text-danger ml-3"><b> Offline <br> <small v-if="user.last_connection">Last seen: {{last_online_timezone}}</small></b></p>
			<b-row id="photos">
				<b-col>
					<b-img v-if="user.profile_image" v-bind:src="user.profile_image" fluid alt="Profile image" width="300"></b-img>
					<small v-else>User has no profile image</small>
				</b-col>
				<b-col>
					<b-img ref="big_photo" fluid alt="First image" width="200" rounded
						v-if="user.images.length > 0"
						v-bind:id="user.images[0].id"
						v-bind:src="user.images[0].src"
					></b-img>
					<small v-else>No images</small>
					<b-row>

					</b-row>
					<b-row v-if="user.images.length > 0">
						<img alt="image" height="80"
							v-on:click="selectPhoto(image.src, image.id)"
							v-for="image in user.images"
							v-bind:src="image.src"
							v-bind:key="image.id"
						/>
					</b-row>
				</b-col>
			</b-row>
			<b-row>
				<b-col cols="7">
					<div class="details"> <b> Rating: </b> {{user.rating}} / 10 </div>
					<div class="details"> <b> Name: </b> {{user.first_name}} {{user.last_name}}</div>
					<div class="details"> <b> Gender: </b> {{user.gender}}</div>
					<div class="details"> <b> Age: </b> {{user.age}}</div>
					<div class="details" v-if="sexualPref(user.sex_pref, user.gender)"> <b> I date: </b> {{i_date}} </div>
					<div class="details"><b-col><b-row>
						<b> About me: </b><b-col cols="11">{{user.bio_text}}</b-col>
					</b-row></b-col></div>
					<div class="details">
						<p class="one_line"><b> My tags: </b></p>
						<ul class="tags" v-for="tag in user.tags" :key="tag">
							<li> #{{tag}} </li>
						</ul>
					</div>
				</b-col>
				<b-col class="mt-5" v-if="users_can_chat">
					<router-link v-bind:to="'/chat/' + id">
						<b-button variant="success" size="lg" class="mt-5">Go to chat!</b-button>
					</router-link>
				</b-col>
			</b-row>
			<b-row>
				<b-col><div class="details">
					<p class="text-danger" v-if="no_photo">Please, upload profile image before liking another user</p>
					<p class="text-danger" v-if="is_blocked">You can't like user who blocked you</p>
					<p class="one_line">Do you like me?</p>
					<!--                <div v-on:click="user.has_like = !user.has_like">-->
					<div v-on:click="changeLikeState">
						<img v-if="user.has_like" src="../assets/heart_red.png" width="40" alt="liked">
						<img v-else src="../assets/heart_white.png" width="40" alt="not liked">
					</div>
					<div class="mt-3" id="am_i_liked">
						<small class="likes_me" v-if="user.likes_me"> P.S. <b>{{user.first_name}} {{user.last_name}}</b> likes you :) </small>
						<small class="likes_me" v-else> <b>{{user.first_name}} {{user.last_name}}</b> didn't like you yet... </small>
					</div>
				</div></b-col>
			</b-row>
			<div id="report" class="mt-5" v-if="!user.is_blocked">
				<a href="#" v-on:click="reportFake"><small> Report user as fake </small></a>
				<br>
				<a href="#" v-on:click="blockUser"><small> Block user </small></a>
			</div>
			<div class="mt-5" v-else>
				<p class="text-danger">You blocked or reported this user as fake. <a href="#" v-on:click="undoBlock">Undo</a></p>
			</div>
		</div>
	</div>
</template>

<script>
	import axios from 'axios';

	export default {
		name: "CheckProfile.vue",
		data() {
			return {
				users_can_chat: null,
				user_not_exist: null,
				no_photo: null,
				is_blocked: null,
				big_photo: '',
				i_date: '',
				id: this.$route.params.id,
				last_online_timezone: null,
				user: {
					images: [{id: null, src: null}],
				},
			}
		},
		methods: {
			selectPhoto(src, id) {
				this.$refs['big_photo'].src = src;
				this.$refs['big_photo'].id = id;
			},

			sexualPref(my_pref, gender) {
				if (gender === 'female' && my_pref === 'hetero') {
					return this.i_date = 'boys'
				}
				if (gender === 'male' && my_pref === 'hetero') {
					return this.i_date = 'girls'
				}
				if (gender === 'male' && my_pref === 'homo') {
					return this.i_date = 'boys'
				}
				if (gender === 'female' && my_pref === 'homo') {
					return this.i_date = 'girls'
				}
				if (my_pref === 'bi') {
					return this.i_date = 'boys and girls'
				}
			},
			getUser() {
				axios.get(this.$root.API_URL + '/users/' + this.id, {
					params: {
						with_images: true,
						with_like: true,
						with_block: true
					},
					withCredentials: true
				})
					.then(response => {
						this.user = response.data.user;

						const moment = require('moment');
						this.last_online_timezone =  moment.utc(this.user.last_connection).tz("Europe/Paris").format('LLL');
					})
					.catch(error => {
						if (error.response.status === 404) {
							this.user_not_exist = true;
						}
					});
			},
			changeLikeState() {
				// Add like
				if (this.user.has_like === false) {
					axios.post(this.$root.API_URL + '/likes/' + this.id, {}, {
						withCredentials: true
					})
						.then(() => {
							this.user.has_like = true;
							this.usersCanChat();
						})
						.catch(error => {
							if (error.response.status === 403) {
								this.is_blocked = true;
								this.$notify({group: 'foo', type: 'error', title: 'User blocked you', text: 'You cannot connect with user who blocked you', duration: 3000});
							}
							if (error.response.status === 401) {
								this.no_photo = true;
								this.$notify({group: 'foo', type: 'error', title: 'Upload profile image', text: 'You cannot connect with another user without profile image', duration: 3000});
							}
						});
				}
				// Remove like
				else if (this.user.has_like === true) {
					axios.delete(this.$root.API_URL + '/likes/' + this.id, {
						withCredentials: true
					})
						.then(() => {
							this.user.has_like = false;
							this.usersCanChat();
						}).catch(() => {});
				}
			},
			sendBlockRequest() {
				axios.post(this.$root.API_URL + '/users/block/' + this.id, {}, {
					withCredentials: true
				})
					.then(() => {
						this.user.is_blocked = true;
						this.usersCanChat();
					}).catch(() => {});
			},
			reportFake() {
				let popup = confirm("This account will be reported as fake and will not appear in your search anymore");
				if (popup === true) {
					this.sendBlockRequest();
				}
			},
			blockUser() {
				let popup = confirm("This account will be blocked. It will not appear in your search anymore, and will not generate any notifications");
				if (popup === true) {
					this.sendBlockRequest();
				}
			},
			undoBlock() {
				axios.delete(this.$root.API_URL + '/users/block/' + this.id, {
					withCredentials: true
				})
					.then(() => {
						this.user.is_blocked = false;
						this.usersCanChat();
					}).catch(() => {});
			},
			usersCanChat() {
				axios.get(this.$root.API_URL + '/messages/allowed/' + this.id, {
					withCredentials: true
				})
				.then(response => {
					if (response.status === 200 && response.data.ok === true)
						this.users_can_chat = true;
					else if (response.status === 200 && response.data.ok === false)
						this.users_can_chat = false;
				}).catch(() => {});
			}
		},
		created() {
			this.getUser();
			this.usersCanChat();
		}
	}
</script>

<style scoped>
	#photos {
		margin: 30px;
	}

	.one_line {
		float: left;
	}

	.tags {
		padding: 0 0 0 8px;
		float: left;
		list-style-type: none;
	}

	.details {
		margin-bottom: 5px;
		margin-top: 10px;
	}

	.likes_me {
		color: #eb6562;
	}
</style>
