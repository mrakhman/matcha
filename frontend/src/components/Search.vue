<template>
    <div class="main">
        <h3 class="title"> Search </h3>
        <br>
        <b-form v-on:submit.prevent="sendSortFilter">
    <!-- AGE container -->
            <b-container id="age" class="bv-example-row" fluid>
                <b-row class="mb-3">
                    <b-col md="6">
                        <b-row>
                            <h4><b>Age:</b></h4>
                            <b-col cols="3">
                                <b-form-input size="sm" type="number" disabled v-model="filter.age.min"></b-form-input>
                            </b-col>
                            <h4>&ndash;</h4>
                            <b-col cols="3">
                                <b-form-input size="sm" type="number" disabled v-model="filter.age.max"></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
                </b-row>

                <b-row>
                    <b-col cols="10">
                        <b-row>
                        <label for="age_min">From</label>
                            <b-col cols="5">
                                <b-form-input id="age_min" type="range"
                                              v-model="filter.age.min"
                                              v-bind:min="sort_options[1].min"
                                              v-bind:max="Math.min(sort_options[1].max, filter.age.max)"
                                ></b-form-input>
                            </b-col>
                            <label for="age_max">To</label>
                            <b-col cols="5">
                                <b-form-input id="age_max" type="range"
                                          v-model="filter.age.max"
                                          v-bind:min="Math.max(sort_options[1].min, filter.age.min)"
                                          v-bind:max="sort_options[1].max"
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
                    <b-col md="6">
                        <b-row>
                            <h4><b>Fame rating:</b></h4>
                            <b-col cols="3">
                                <b-form-input size="sm" type="number" disabled v-model="filter.rating.min"></b-form-input>
                            </b-col>
                            <h4>&ndash;</h4>
                            <b-col cols="3">
                                <b-form-input size="sm" type="number" disabled v-model="filter.rating.max"></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
<!--                    <b-col xl="7"></b-col>-->

                </b-row>

                <b-row>
                    <b-col cols="10">
                        <b-row>
                            <label for="rating_min">From</label>
                            <b-col cols="5">
                                <b-form-input id="rating_min" type="range"
                                              v-model="filter.rating.min"
                                              v-bind:min="sort_options[2].min"
                                              v-bind:max="Math.min(sort_options[2].max, filter.rating.max)"
                                ></b-form-input>
                            </b-col>
                            <label for="rating_max">To</label>
                            <b-col cols="5">
                                <b-form-input id="rating_max" type="range"
                                              v-model="filter.rating.max"
                                              v-bind:max="sort_options[2].max"
                                              v-bind:min="Math.max(sort_options[2].min, filter.rating.min)"
                                ></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
<!--                    <b-col xl="4"></b-col>-->

                </b-row>
            </b-container>

            <br>
            <br>

    <!-- DISTANCE container -->
            <b-container id="distance" class="bv-example-row" fluid>
                <b-row>
                    <b-col md="12">
                        <b-row>
                            <h4><b>Max distance (km):</b></h4>
                            <b-col md="4">
                                <b-form-input type="number" v-model="filter.distance.max"></b-form-input>
                            </b-col>
                        </b-row>
                    </b-col>
<!--                    <b-col xl="6"></b-col>-->
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
            <b-button type="submit" variant="primary">Sort</b-button>
        </b-form>
        <hr>
    </div>
</template>

<script>
    export default {
        name: "Search.vue",
        props: ['sort_form','filter', 'tags'],
        data() {
            return {
                sort_options: [
                    { value: 'my_tags', text: 'My tags matches'},
                    { value: 'age', text: 'Age', min: 0, max: 99},
                    { value: 'rating', text: 'Fame rating', min: 0, max: 10},
                    { value: 'distance', text: 'Distance', min: 0, max: 10000},
                    { value: 'tags', text: 'Tags'}
                ],
                tag_options: ['42', 'eco', 'geek', 'veggie', 'music', 'travel'],
            }
        },
        methods: {
            validateDistance() {
                if(this.filter.distance.max < 0)
                    this.filter.distance.max = 0
            },

            sendSortFilter() {
                this.validateDistance();
                let sort = this.sort_form;
                let filter = this.filter;
                this.$emit('sendSortFilter', sort, filter)
            }
        },
        created() {
        },
    }
</script>

<style scoped>

</style>
