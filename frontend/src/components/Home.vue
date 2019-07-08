<template>
    <div class="main">
        <h3>I am a very empty page</h3>
        <p id="demo">{{geo}}</p>
        <h4>{{lat}}</h4>
        <h4>{{lon}}</h4>
    </div>
</template>

<script>
    export default {
        name: "Home.vue",
        data () {
            return {
                geo: null,
                lat: null,
                lon: null,
                geo_options: {
                    enableHighAccuracy: true,
                    maximumAge        : 30000,
                    timeout           : 27000
                },
            }
        },
        methods: {
            showPosition(position) {
                this.lat = position.coords.latitude;
                this.lon = position.coords.longitude;
            },
            geo_error() {
                alert("Sorry, no position available.");
            },

        },
        created() {
            if ("geolocation" in navigator) {
                this.geo = "geolocation is available"
            } else {
                this.geo = "geolocation is NOT available"
            }

            if(navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(this.showPosition, this.geo_error, this.geo_options);
            }
            else {
                this.geo = "Geolocation is not supported."
            }
        }
    }
</script>

<style scoped>

</style>
