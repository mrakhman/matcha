<template>
    <div class="main">
        <Search
                v-on:sendSortFilter="updateFilters"
                :filter="filter"
                :sort_form="sort_form"
        />
        <pre class="mt-3 mb-0">{{ users.length }}</pre>
        <pre class="mt-3 mb-0">{{ total_users }}</pre>
        <pre class="mt-3 mb-0">{{ per_page }}</pre>
        <h3> Users List </h3>
        <b-row>
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
                        {{user.age}} <br>
                        {{user.gender}} <br>
                        {{user.tags}} <br>
                        {{user.sex_pref}}
                    </b-card-text>
                    <router-link v-bind:to="'users/' + user.id"><b-button variant="outline-primary">Open</b-button></router-link>
                </b-card>
            </div>
        </b-row>
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

export default {
    name: "UsersList.vue",
    components: {
        Search
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
                order_by: 'asc',
                sort_by: 'my_tags'
            },
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
        // updateUserList(response_data) {
        //     this.users = response_data["users"];
        //     this.total_users = response_data["total_users"];
        //     this.per_page = response_data["per_page"];
        // }
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
