<template>
    <div class="main">
        <b-container class="bv-example-row" fluid>
            <b-row>
                <b-col xl="7">
                    <b-row>
                        <label for="age-1">Age: between 18 and 99</label>
                        <b-col>
                            <b-form-input id="age-1" type="number"
                                          v-model="form.age.min"
                                          v-bind:min="sort.by[0].min"
                                          v-bind:max="min(sort.by[0].max, form.age.max)"
                            ></b-form-input>
<!--                            v-if="form.age.min"-->

                        </b-col>
                        <h3> - </h3>
                        <b-col>
                            <b-form-input id="age-2" type="number"
                                          v-model="form.age.max"
                                          v-bind:min="max(sort.by[0].min, form.age.min)"
                                          v-bind:max="sort.by[0].max"
                            ></b-form-input>
                        </b-col>
                    </b-row>
                </b-col>
            </b-row>

            <b-row>
                <b-col xl="7">
                    <label for="range_min">Example range with min and max</label>
                    <b-form-input id="range_min" v-model="filter.value" type="range" v-bind:min="sort.by[0].min" v-bind:max="sort.by[0].max"></b-form-input>
                    <b-form-input id="range_max" v-model="filter.value" type="range" min="0" max="5"></b-form-input>
                    <div class="mt-2">Value: {{ filter.value }}</div>
                </b-col>
            </b-row>
        </b-container>
        <hr>

        <b-container>
            <b-form @submit.prevent="">
                <h4><b>Sort</b></h4>
                <b-row>
                    <b-col xl="2">
                        <label for="order">Order:</label>
                        <b-form-group id="order">
                            <b-form-radio v-model="sort.selected" name="some-radios" value="asc">Asc</b-form-radio>
                            <b-form-radio v-model="sort.selected" name="some-radios" value=desc>Desc</b-form-radio>
                        </b-form-group>
                    </b-col>
                    <b-col xl="3">
                        <label for="sort-by">Sort by:</label>
                        <b-form-select id="sort-by" v-bind:options="sort.by" class="mt-3"></b-form-select>
                    </b-col>
                </b-row>
            </b-form>
        </b-container>
        <pre class="mt-3 mb-0">{{ sort }}</pre>
        <hr>
    </div>
</template>

<script>
    export default {
        name: "Search.vue",
        data() {
            return {
                sort: {
                    selected: 'asc',
                    by: [
                        { value: 'age', text: 'Age', min: 18, max: 99},
                        { value: 'rating', text: 'Fame rating', min: 0, max: 10},
                        { value: 'distance', text: 'Distance', min: 0, max: 1000}
                    ],
                },
                filter: {
                    value: null
                },
                form: {
                    age: {
                        min: null,
                        max: null
                    }
                }
            }
        }
    }
</script>

<style scoped>

</style>