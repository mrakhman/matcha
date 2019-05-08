import MyProfile from './components/MyProfile.vue';
import Header from "./components/Header";
// import Login from "./components/Login";
import Register from "./components/Register";
import ViewProfile from "./components/ViewProfile";

// We can just register the array [{}, {}] in main.js inside "const router = new VueRouter({ ..."
// without creating a separate file routes.js

export default [
    { path: '/', component: Register},
    { path: '/my_profile', component: MyProfile},
    { path: '/view_profile', component: ViewProfile},
    { path: '/header', component: Header}
]
