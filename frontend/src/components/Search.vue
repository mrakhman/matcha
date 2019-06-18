<template>
    <div class="main">
        <b-form v-on:submit.prevent="submitSortFilter">
    <!-- AGE container -->
            <b-container id="age" class="bv-example-row" fluid>
                <b-row class="mb-3">
                    <b-col xl="5">
                        <b-row>
                            <h4><b>Age</b></h4>
                            <b-col xl="2">
                                <b-form-input size="sm" type="number" disabled v-model="filter.age.min"></b-form-input>
                            </b-col>
                            <h4>&ndash;</h4>
                            <b-col xl="2">
                                <b-form-input size="sm" type="number" disabled v-model="filter.age.max"></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
                </b-row>

                <b-row>
                    <b-col xl="8">
                        <b-row>
                        <label for="age_min">From</label>
                            <b-col xl="4">
                                <b-form-input id="age_min" type="range"
                                              v-model="filter.age.min"
                                              v-bind:min="sort_options[0].min"
                                              v-bind:max="Math.min(sort_options[0].max, filter.age.max)"
                                ></b-form-input>
                            </b-col>
                            <label for="age_max">To</label>
                            <b-col xl="4">
                                <b-form-input id="age_max" type="range"
                                          v-model="filter.age.max"
                                          v-bind:min="Math.max(sort_options[0].min, filter.age.min)"
                                          v-bind:max="sort_options[0].max"
                                ></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
                </b-row>
            </b-container>

            <br>
            <br>

    <!-- RATING container -->
            <b-container id="rating" class="bv-example-row" fluid>
                <b-row class="mb-3">
                    <b-col xl="5">
                        <b-row>
                            <h4><b>Fame rating</b></h4>
                            <b-col xl="2">
                                <b-form-input size="sm" type="number" disabled v-model="filter.rating.min"></b-form-input>
                            </b-col>
                            <h4>&ndash;</h4>
                            <b-col xl="2">
                                <b-form-input size="sm" type="number" disabled v-model="filter.rating.max"></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
                </b-row>

                <b-row>
                    <b-col xl="8">
                        <b-row>
                            <label for="rating_min">From</label>
                            <b-col xl="4">
                                <b-form-input id="rating_min" type="range"
                                              v-model="filter.rating.min"
                                              v-bind:min="sort_options[1].min"
                                              v-bind:max="Math.min(sort_options[1].max, filter.rating.max)"
                                ></b-form-input>
                            </b-col>
                            <label for="rating_max">To</label>
                            <b-col xl="4">
                                <b-form-input id="rating_max" type="range"
                                              v-model="filter.rating.max"
                                              v-bind:max="sort_options[1].max"
                                              v-bind:min="Math.max(sort_options[1].min, filter.rating.min)"
                                ></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
                </b-row>
            </b-container>

            <br>
            <br>

    <!-- DISTANCE container -->
            <b-container id="distance" class="bv-example-row" fluid>
                <b-row>
                    <b-col xl="6">
                        <b-row>
                            <h4><b>Distance</b></h4>
                            <b-col xl="2">
                                <b-form-input size="sm" type="number" disabled v-model="filter.distance.min"></b-form-input>
                            </b-col>
                            <h4>&ndash;</h4>
                            <b-col xl="2">
                                <b-form-input size="sm" type="number" disabled v-model="filter.distance.max"></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
                </b-row>

                <b-row>
                    <b-col xl="8">
                        <b-row>
                            <label for="distance_min">From</label>
                            <b-col xl="4">
                                <b-form-input id="distance_min" type="range"
                                              v-model="filter.distance.min"
                                              v-bind:min="sort_options[2].min"
                                              v-bind:max="Math.min(sort_options[2].max, filter.distance.max)"
                                ></b-form-input>
                            </b-col>
                            <label for="distance_max">To</label>
                            <b-col xl="4">
                                <b-form-input id="distance_max" type="range"
                                              v-model="filter.distance.max"
                                              v-bind:max="sort_options[2].max"
                                              v-bind:min="Math.max(sort_options[2].min, filter.distance.min)"
                                ></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
                </b-row>
            </b-container>

            <br>

            <!-- TAGS container -->
            <b-container id="tags" class="bv-example-row" fluid>
                <b-row>
                    <b-col xl="6">
                        <b-row>
                            <h4><b>Tags</b></h4>
                        </b-row>
                        <b-row>
                            <b-form-checkbox-group
                                    v-model="filter.tags"
                                    :options="tags_options"
                                    name="flavour-1a"
                            ></b-form-checkbox-group>
                        </b-row>
                    </b-col>
                </b-row>
            </b-container>
            <br>

            <b-button type="submit" variant="primary">Apply filters</b-button>
        </b-form>
<!-- END -->
        <hr>

        <b-form v-on:submit.prevent="submitSortFilter">
<!--            <b-container>-->
                <h4><b>Sort by</b></h4>
                <b-row>
                    <b-col xl="3">
                        <b-form-select id="sort-by" v-model="sort_form.sort_by" v-bind:options="sort_options" class="mt-1"></b-form-select>
                    </b-col>
                    <b-col xl="2">
                        <b-form-group id="order">
                            <b-form-radio v-model="sort_form.order_by" name="some-radios" value="asc">Asc &#8648;</b-form-radio>
                            <b-form-radio v-model="sort_form.order_by" name="some-radios" value=desc>Desc &#8650;</b-form-radio>
                        </b-form-group>
                    </b-col>
                </b-row>
<!--            </b-container>-->
            <b-button type="submit" variant="primary">Sort</b-button>
        </b-form>
        <pre class="mt-3 mb-0">{{ sort_form }}</pre>
        <pre class="mt-3 mb-0">{{ filter }}</pre>
        <hr>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Search.vue",
        data() {
            return {
                sort_options: [
                        { value: 'age', text: 'Age', min: 0, max: 99},
                        { value: 'rating', text: 'Fame rating', min: 0, max: 10},
                        { value: 'distance', text: 'Distance', min: 0, max: 100}
                    ],
                tags_options: ['eco', 'geek', 'veggie', 'travel', '42', 'music'],
                sort_form: {
                    order_by: 'asc',
                    sort_by: 'id'
                },
                filter: {
                    age: { min: 0, max: 99},
                    rating: { min: 0, max: 10},
                    distance: { min: 0, max: 100},
                    // tags: []
                }
            }
        },
        methods: {
            // submitFilter() {
            //     // if (this.sort_form.sort_by === null) {
            //     //     return(this.$notify({group: 'foo', type: 'error', title: 'Empty sort', text: 'Select field to sort by', duration: -1}))
            //     // }
            //     axios.post(this.$root.API_URL + '/users/masha', {
            //         filter: this.filter
            //     }, {withCredentials: true})
            //         .then(response => {
            //             if(response.status === 200)
            //             {
            //                 this.$notify({group: 'foo', type: 'success', title: 'Success', text: 'Users are sorted', duration: 2000})
            //                 // response.data ...
            //             }
            //             // TODO: console
            //             console.log(response)
            //         })
            //         .catch(error => {
            //
            //             // TODO: console
            //             console.log(error)
            //         })
            // },

            submitSortFilter() {
                axios.post(this.$root.API_URL + '/users/filter/page/0', {
                    sort: this.sort_form,
                    filter: this.filter
                }, {withCredentials: true})
                    .then(response => {
                        if(response.status === 200)
                        {
                            this.$notify({group: 'foo', type: 'success', title: 'Success', text: 'Users are sorted', duration: 2000});
                            var response_data = response.data;
                            this.$emit('updateUserList', response_data);
                        }
                        // TODO: console
                        console.log(response)
                    })
                    .catch(error => {

                        // TODO: console
                        console.log(error)
                    })
            }
        }
    }
</script>

<style scoped>

</style>
