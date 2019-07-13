<template>
    <div class="main">
        <Location/>
    </div>
</template>

<script>
    import axios from 'axios';
    import Location from './Location';
    export default {
        name: "Home.vue",
        components: {
            Location
        },
        data () {
            return {
                // geo_info: null,
                // lat: null,
                // lon: null,
                // geo_options: {
                //     enableHighAccuracy: true,
                //     maximumAge        : 300000, // 5 * 60 * 1000 = 5 min
                //     timeout           : 27000 // 27 * 1000 = 27 sec
                // },
                // watchID: null,
                //
                //
                // address: null,
                // // search_lat: 48.896652,
                // // search_lon: 2.318356,
                // search_lat: null,
                // search_lon: null,
                // empty_address: null,
                // error_request: null,
            }
        },
        methods: {}
    }
</script>

<style scoped>

</style>
