<template>
    <div class="main">
        <Location/>
        <Search
                v-on:sendSortFilter="updateFilters"
                :filter="filter"
                :sort_form="sort_form"
        />
        <pre class="mt-3 mb-0">total: {{ total_users }}, per_page: {{ per_page }}</pre>
        <h3> Users List </h3>
        <b-row v-if="users.length > 0">
            <div id="users_list"
                 v-for="user in users"
                 :key="user.id"
                 :current-page="current_page"
                 :per-page="per_page"
                 :items="users"
            >

                <b-card v-bind:title="user.first_name + ' ' + user.last_name"
                        v-bind:img-src="user.profile_image"
                        img-alt="profile picture"
                        style="max-width: 15rem;"
                        class="mb-2 add_space"
                >
                    <b-card-text>
                        Age: {{user.age}} <br>
                        Rating: {{user.rating}}/10 <br>
                        Gender: {{user.gender}} <br>
                        I am: {{user.sex_pref}} <br>
                        {{user.tags}} <br>
                    </b-card-text>
                    <router-link v-bind:to="'users/' + user.id"><b-button variant="outline-primary">Open</b-button></router-link>
                </b-card>
            </div>
        </b-row>
        <div v-else class="mb-3"> No users matched your search :( </div>
        <div>
            <b-pagination
                    v-model="current_page"
                    :total-rows="total_users"
                    :items="users"
                    :per-page="per_page"
                    v-on:input="getUsers"
                    aria-controls="users_list"
            ></b-pagination>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
import Search from "./Search";
import Location from './Location';

export default {
    name: "UsersList.vue",
    components: {
        Search,
        Location
    },
    data() {
        return {
            current_page: 1,
            per_page: 0,
            total_users: 0,
            users: [],

            filter: {
                age: { min: 0, max: 99},
                rating: { min: 0, max: 10},
                distance: { min: 0, max: 100},
                tags: []
            },
            sort_form: {
                order_by: 'desc',
                sort_by: 'my_tags'
            },
            i_date: '',
            lat: null,
            lon: null
        }
    },

    methods: {
        updateFilters(sort, filter) {
            this.sort_form = sort;
            this.filter = filter;
            this.current_page = 1;
            this.getUsers();
        },
        getUsers() {
            axios.post(this.$root.API_URL + '/users/filter/page/' + (this.current_page - 1), {
                filter: this.filter,
                sort: this.sort_form
            }, {withCredentials: true})
                .then(response => {
                    this.users = response.data["users"];
                    this.total_users = response.data["total_users"];
                    this.per_page = response.data["per_page"];
                    console.log(response);
                })
                // TODO: console
                // eslint-disable-next-line
                .catch(error => console.log(error));
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
        },
        ipLocation() {
            axios.get('https://europe-west1-matcha-246115.cloudfunctions.net/geolocation')
                    .then(response => {
                        if(response.status === 200)
                        {
                            let lat_long = response.data.cityLatLong;
                            lat_long = lat_long.split(",");
                            this.lat = lat_long[0];
                            this.lon = lat_long[1];
                        }
                    })
                    .catch(error => {
                        // TODO: console
                        console.log(error)
                    })
        }
    },

    created() {
        this.getUsers();
    }
}
</script>

<style scoped>
    .add_space {
        margin: 10px;
    }

</style>
