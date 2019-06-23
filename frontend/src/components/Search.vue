<template>
    <div class="main">
        <b-form v-on:submit.prevent="sendSortFilter">
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
                                    :options="tag_options"
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

        <b-form v-on:submit.prevent="sendSortFilter">
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
    // import axios from 'axios';

    export default {
        name: "Search.vue",
        props: ['sort_form','filter', 'tags'],
        data() {
            return {
                sort_options: [
                    { value: 'age', text: 'Age', min: 0, max: 99},
                    { value: 'rating', text: 'Fame rating', min: 0, max: 10},
                    { value: 'distance', text: 'Distance', min: 0, max: 100},
                    { value: 'tags', text: 'Tags'}
                ],
                tag_options: ['42', 'eco', 'geek', 'veggie', 'music', 'travel'],
                // tags: [
                //     {tag_id: 1, tag: '42'},
                //     {tag_id: 2, tag: 'eco'},
                //     {tag_id: 3, tag: 'geek'},
                //     {tag_id: 4, tag: 'veggie'},
                //     {tag_id: 5, tag: 'music'},
                //     {tag_id: 6, tag: 'travel'}
                // ],
                // sort_form: {
                //     order_by: 'asc',
                //     sort_by: 'id'
                // },
                // filter: {
                //     age: { min: 0, max: 99},
                //     rating: { min: 0, max: 10},
                //     distance: { min: 0, max: 100},
                //     // tags: []
                // }
            }
        },
        methods: {
            sendSortFilter() {
                var sort = this.sort_form;
                var filter = this.filter;
                // console.log(sort, filter);
                this.$emit('sendSortFilter', sort, filter)
            }
        }
    }
</script>

<style scoped>

</style>
