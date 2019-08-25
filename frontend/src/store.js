import Vue from 'vue'
import Vuex from "vuex";
import axios from 'axios'

import {API_URL} from "./vars";

Vue.use(Vuex);


const store = new Vuex.Store({
    state: {
        initialized: false,
        user: {},
        logged_in: false,
    },
    mutations: {
        update_user(state, user) {
            state.user = {...state.user, ...user};
        },
        login(state) {
            state.logged_in = true;
        },
        logout(state) {
            state.user = {};
            state.logged_in = false;
        },
        initialize(state) {
            state.initialized = true;
        }

    },
    actions: {
        update_user({state, commit}) {
            const logged_in = state.logged_in;
            const initialized = state.initialized;
            return axios.get(`${API_URL}/users/me`, {withCredentials: true})
                .then(response => {
                    let user = response.data["user"];
                    user.dob = user.dob ? user.dob.substring(0, 10) : null;
                    commit('update_user', user);

                    if (!logged_in) {
                        commit('login');
                    }
                    if (initialized) {
                        commit('initialize');
                    }
                })
                .catch(() => {
                    if (initialized) {
                        commit('initialize');
                    }
                });
        }
    }
});

export default store;
