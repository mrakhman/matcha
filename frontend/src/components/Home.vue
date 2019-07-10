<template>
    <div class="main">
        <h3>Check your location</h3>
        <pre>hello, {{watchID}}</pre>
        <p id="demo">{{geo}}</p>
        <h4>{{lat}}</h4>
        <h4>{{lon}}</h4>
        <iframe
            v-if="lon && lat"
            width="600"
            height="450"
            frameborder="0" style="border:0"
            :src="'https://www.google.com/maps/embed/v1/place?key=AIzaSyDxxEhAC0zLdWys3h-ry5jBzbcQObyrDOY&q=' + number_lat + ',' + number_lon">
        </iframe>

        <h3>popa</h3>

        <b-row class="main">
            <b-col xl="8">
                <b-row>
                    <label for="lat">Lat</label>
                    <b-col xl="4">
                        <b-form-input id="lat" type="number" v-model="number_lat"></b-form-input>
                    </b-col>
                    <label for="lon">Lon</label>
                    <b-col xl="4">
                        <b-form-input id="lon" type="number" v-model="number_lon"></b-form-input>
                    </b-col>
                </b-row>
            </b-col>
        </b-row><br>

    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: "Home.vue",
        data () {
            return {
                number_lon: null,
                number_lat: null,
                geo: null,
                lat: null,
                lon: null,
                geo_options: {
                    // enableHighAccuracy: true,
                    maximumAge        : 300000, // 5 * 60 * 1000 = 5 min
                    timeout           : 27000 // 27 * 1000 = 27 sec
                },
                watchID: null
            }
        },
        methods: {
            showPosition(position) {
                this.lat = position.coords.latitude;
                this.lon = position.coords.longitude;
            },
            geoError() {
                this.geo = "You chose not to detect your location (or request timed out)"
            },
            sendLocation() {
                if(this.lat && this.lon) {
                    axios.post(this.$root.API_URL + '/users/location', {
                        latitude: this.lat,
                        longitude: this.lon
                    }, {withCredentials: true})
                        .then(response => {
                            if(response.status === 200)
                            {
                                this.$notify({group: 'foo', type: 'success', title: 'Saved', text: 'Location updated!', duration:3000});
                            }
                            // TODO: console
                            console.log(response)
                        })
                        .catch(error => {
                            this.$notify({group: 'foo', type: 'error', title: 'Error', text: 'Some error...', duration: 3000});
                            // TODO: console
                            console.log(error)
                        })
                }
            },
            getLocation() {
                if ("geolocation" in navigator) {
                    this.geo = "Geolocation is available"
                } else {
                    this.geo = "Geolocation is not available"
                }

                if(navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(this.showPosition, this.geoError, this.geo_options);
                }
                else {
                    this.geo = "Geolocation is not supported."
                }
            },
            watchLocation() {
                this.watchID = navigator.geolocation.watchPosition(this.showPosition, this.geoError, this.geo_options);
                this.sendLocation();
            }

        },
        created() {
            this.getLocation();

        },
        beforeUpdate() {
            this.watchLocation();
        }
    }
</script>

<style scoped>

</style>
