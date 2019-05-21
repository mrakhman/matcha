import MyProfile from './components/MyProfile.vue';
import Header from "./components/Header";
// import Login from "./components/Login";
import Register from "./components/Register";
import ViewProfile from "./components/ViewProfile";
import ForgotPassword from "./components/ForgotPassword";
import UsersList from "./components/UsersList";
import Login from "./components/Login";
// import Settings from "./components/Settings";
// import AboutMe from "./components/AboutMe";

// We can just register the array [{}, {}] in main.js inside "const router = new VueRouter({ ..."
// without creating a separate file router.js

export default [
    { path: '/register', component: Register},
    { path: '/', component: Register},
    { path: '/login', component: Login},
    { path: '/my_profile', component: MyProfile},
    // { path: '/my_profile/settings', component: Settings},
    // { path: '/my_profile/about_me', component: AboutMe},
    { path: '/view_profile', component: ViewProfile}, // This can be deleted
    { path: '/header', component: Header},
    { path: '/forgot_password', component: ForgotPassword},
    { path: '/users', component: UsersList},
    { path: '/users/:id', component: ViewProfile}
]
