import MyProfile from './components/MyProfile.vue';
import Header from "./components/Header";
import Login from "./components/Login";

// We can just register the array [{}, {}] in main.js inside "const router = new VueRouter({ ..."
// without creating a separate file routes.js

export default [
    { path: '/', component: Login},
    { path: '/my_profile', component: MyProfile},
    { path: '/header', component: Header}
]
