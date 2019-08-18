<template>
    <div class="main">
        <h3>Tell us your location</h3>
        <p>We will be able to show you closest users</p>
        <p class="text-info" id="demo">{{geo_info}}</p>
        <p v-if="no_permissions" class="text-warning">Allow location in your browser so that we can find you</p>
        <b-button class="mb-3" v-on:click="handler('getLocation', 'handlePermission')" variant="outline-primary">Find me</b-button>
        <h4 class="mt-2">Search your location</h4>
        <p class="text-danger m-2" v-if="error_request">Nothing found for your search</p>
        <b-row>
            <b-col xl="6">
                <b-row class="m-2">
                    <label for="address">Enter address</label>
                    <b-form-input class="mb-2" id="address" type="text" v-model="address"></b-form-input>
                    <b-button variant="outline-primary"
                              v-bind:disabled="!address"
                              v-on:click="getLocationByAddress"
                    >Search</b-button>
                    <small class="text-danger m-2" v-if="empty_address">Enter address</small>
                </b-row>
            </b-col>
        </b-row>

        <br>

        <h5 v-if="(lat && lon) && (!search_lat && !search_lon)"><b>My location:</b> {{lat}}, {{lon}}</h5>
        <h5 v-if="search_lat && search_lon"><b>Search location:</b> {{search_lat}}, {{search_lon}}</h5>
        <iframe
                v-if="(lat && lon) && (!search_lat && !search_lon)"
                width="800"
                height="300"
                frameborder="0" style="border:0"
                :src="'https://www.google.com/maps/embed/v1/place?key=AIzaSyDxxEhAC0zLdWys3h-ry5jBzbcQObyrDOY&q=' + lat + ',' + lon">
        </iframe>
        <iframe
                v-if="(search_lat && search_lon)"
                width="800"
                height="300"
                frameborder="0" style="border:0"
                :src="'https://www.google.com/maps/embed/v1/place?key=AIzaSyDxxEhAC0zLdWys3h-ry5jBzbcQObyrDOY&q=' + search_lat + ',' + search_lon">
        </iframe>



        <b-row>
            <b-col>
                <b-button block variant="success"
                          v-bind:disabled="(!lat || !lon) && (!search_lat || !search_lon)"
                          v-on:click="saveLocation(search_lat ? search_lat : lat, search_lon ? search_lon : lon)"
                >Save my location</b-button>
            </b-col>
            <b-col id="empty_column">
            </b-col>
        </b-row>
        <hr>
    </div>
</template>

<script>
    export default {
		name: "Location.vue",
		data () {
			return {
				geo_info: null,
				lat: null,
				lon: null,
				geo_options: {
					enableHighAccuracy: true,
					maximumAge        : 300000, // 5 * 60 * 1000 = 5 min
					timeout           : 27000 // 27 * 1000 = 27 sec
				},
				watchID: null,

				address: null,
				search_lat: null,
				search_lon: null,
				empty_address: null,
				error_request: null,
				no_permissions: null,

                ip_lat: null,
                ip_lon: null,
			}
		},
		methods: {
			handler() {
				this.getLocation();
				this.handlePermission();
			},
			errorCallback(error) {
				switch (error.code) {
					case error.TIMEOUT:
						this.geo_info = "Request timed out";
						navigator.geolocation.getCurrentPosition(this.successCallback, this.errorCallback, this.geo_options);
						break;
					case error.POSITION_UNAVAILABLE:
						this.geo_info = "The position of the device could not be determined";
						break;
					case error.PERMISSION_DENIED:
						this.geo_info = "No permission to use geolocation";
						break;
				}
			},
			successCallback(position) {
				this.lat = position.coords.latitude;
				this.lon = position.coords.longitude;
				this.geo_info = "Coordinates are updated";
			},
			handlePermission() {
				this.no_permissions = null;
				navigator.permissions.query({name:'geolocation'})
                    .then((response) => {
					if (response.state === 'denied')
						this.no_permissions = true;
				});
			},
			getLocation() {
				if(navigator.geolocation) {
					navigator.geolocation.getCurrentPosition(this.successCallback, this.errorCallback, this.geo_options);
					this.search_lat = null;
					this.search_lon = null;
				}
				else {
					this.geo_info = "Geolocation is not supported."
				}
			},
			getLocationByAddress() {
				this.empty_address = null;
				this.error_request = null;
				if(this.address) {
					const googleMapsClient = require('@google/maps').createClient({
						key: 'AIzaSyDxxEhAC0zLdWys3h-ry5jBzbcQObyrDOY',
						Promise: Promise
					});

					googleMapsClient.geocode({address: this.address})
						.asPromise()
						.then((response) => {
							if (response.json.status === "ZERO_RESULTS" ||
								response.json.status === "REQUEST_DENIED" ||
								response.json.status === "ERROR") {
								this.error_request = true;
							}
							if (response.json.status === "OK") {
								this.search_lat = response.json.results[0].geometry.location.lat;
								this.search_lon = response.json.results[0].geometry.location.lng;
							}

						})
						.catch(() => {});
				}
				else {
					this.empty_address = true
				}
			},
			saveLocation(lat, lon) {
                this.$root.axios.post('/settings/location', {
					latitude: lat,
					longitude: lon
				}, {withCredentials: true})
					.then(response => {
						if(response.status === 200)
						{
							this.$notify({group: 'foo', type: 'success', title: 'Saved', text: 'Location updated!', duration:3000});
						}
					})
					.catch(() => {
						this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Some error...', duration: 3000});
					})
			}
	},
		created() {
			this.getLocation();
		}
	}
</script>

<style scoped>

</style>
