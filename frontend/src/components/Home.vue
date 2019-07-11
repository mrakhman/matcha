<template>
    <div class="main">
        <h3>Check your location</h3>
        <b-button block variant="outline-success"
                  v-bind:disabled="(!lat || !lon) && (!search_lat || !search_lon)"
                  v-on:click="saveLocation(search_lat ? search_lat : lat, search_lon ? search_lon : lon)"
        >Save</b-button>
<!--        <pre class="text-danger">Update location, {{watchID}}</pre>-->

        <p id="demo">{{geo_info}}</p>
        <b-button v-on:click="getLocation" variant="outline-primary">Get my location</b-button>
        <h5 v-if="(lat && lon) && (!search_lat && !search_lon)"><b>My location:</b> {{lat}}, {{lon}}</h5>
        <h5 v-if="search_lat && search_lon"><b>Search location:</b> {{search_lat}}, {{search_lon}}</h5>
        <iframe
            v-if="(lat && lon) && (!search_lat && !search_lon)"
            width="600"
            height="450"
            frameborder="0" style="border:0"
            :src="'https://www.google.com/maps/embed/v1/place?key=AIzaSyDxxEhAC0zLdWys3h-ry5jBzbcQObyrDOY&q=' + lat + ',' + lon">
        </iframe>
        <iframe
            v-if="(search_lat && search_lon)"
            width="600"
            height="450"
            frameborder="0" style="border:0"
            :src="'https://www.google.com/maps/embed/v1/place?key=AIzaSyDxxEhAC0zLdWys3h-ry5jBzbcQObyrDOY&q=' + search_lat + ',' + search_lon">
        </iframe>

        <h4 class="mt-4">Search your location</h4>
        <p class="text-danger m-2" v-if="error_request">Nothing found for your search</p>
        <b-row>
            <b-col xl="6">
                <b-row class="m-2">
<!--                    <b-form v-on:submit.prevent="getLocationByAddress">-->
                        <label for="address">Enter address</label>
                        <b-form-input class="mb-2" id="address" type="text" v-model="address"></b-form-input>
<!--                        <b-button variant="primary" type="submit" >Search</b-button>-->
                        <b-button variant="outline-primary"
                                  v-bind:disabled="!address"
                                  v-on:click="getLocationByAddress"
                        >Search</b-button>
                        <small class="text-danger m-2" v-if="empty_address">Enter address</small>
<!--                    </b-form>-->
                </b-row>
            </b-col>
        </b-row><br>

        <b-button block variant="outline-success"
                  v-bind:disabled="(!lat || !lon) && (!search_lat || !search_lon)"
                  v-on:click="saveLocation(search_lat ? search_lat : lat, search_lon ? search_lon : lon)"
        >Save</b-button>

    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: "Home.vue",
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
                // search_lat: 48.896652,
                // search_lon: 2.318356,
                search_lat: null,
                search_lon: null,
                empty_address: null,
                error_request: null,
            }
        },
        methods: {
            // showPosition(position) {
            //     this.lat = position.coords.latitude;
            //     this.lon = position.coords.longitude;
            //
            //     this.geo_info = "Coordinates are updated";
            // },
            // geoError() {
            //     this.geo_info = "You chose not to detect your location";
            // },
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
            getLocation() {
                // if ("geolocation" in navigator) {
                //     this.geo_info = "Geolocation is available, but blocked by user"
                //
                // }
                // else {
                //     this.geo_info = "Geolocation is not available"
                // }
                if(navigator.geolocation) {
                    // navigator.geolocation.getCurrentPosition(this.showPosition, this.geoError, this.geo_options);
                    navigator.geolocation.getCurrentPosition(this.successCallback, this.errorCallback, this.geo_options);
                    this.search_lat = null;
                    this.search_lon = null;
                }
                else {
                    this.geo_info = "Geolocation is not supported."
                }
            },
            watchLocation() {
                if(navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(this.successCallback, this.errorCallback, this.geo_options);
                }
                // this.watchID = navigator.geolocation.watchPosition(this.showPosition, this.geoError, this.geo_options);
                // this.saveLocation();
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
                            // TODO: console
                            console.log(response.json);

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
                        .catch((err) => {
                            // TODO: console
                            console.log(err);
                        });
                }
                else {
                    this.empty_address = true
                }
            },
            saveLocation(lat, lon) {
                // if(this.lat && this.lon) {
                    axios.post(this.$root.API_URL + '/users/location', {
                        latitude: lat,
                        longitude: lon
                    }, {withCredentials: true})
                            .then(response => {
                                if(response.status === 200)
                                {
                                    this.$notify({group: 'foo', type: 'success', title: 'Saved', text: 'Location updated!', duration:3000});
                                    console.log("Saved to db!");
                                }
                                // TODO: console
                                console.log(response)
                            })
                            .catch(error => {
                                this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Some error...', duration: 3000});
                                // TODO: console
                                console.log(error)
                            })
                // }
            },




    },
        created() {
            if (this.getLocation()) {
                this.saveLocation(this.lat, this.lon);
            }

        },
        beforeUpdate() {
            // this.watchLocation(); // TODO: figure our when to update me !!!!!
        }
    }
</script>

<style scoped>

</style>
