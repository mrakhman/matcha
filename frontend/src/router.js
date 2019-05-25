import MyProfile from './components/MyProfile.vue';
// import Header from "./components/Header";
// import Login from "./components/Login";
import Register from "./components/Register";
import ViewProfile from "./components/ViewProfile";
import ForgotPassword from "./components/ForgotPassword";
import UsersList from "./components/UsersList";
import Login from "./components/Login";
// import Settings from "./components/Settings";
// import AboutMe from "./components/AboutMe";
import {Auth} from './auth'
import Home from "./components/Home";

// We can just register the array [{}, {}] in main.js inside "const router = new VueRouter({ ..."
// without creating a separate file router.js

const ifAuthenticated = (to, from, next) => {
    console.log("ifNotAuthenticated");
    console.log("Auth.loggedId: ", Auth.loggedIn);
    if (Auth.loggedIn)
    {
        next();
        return
    }
    next('/login')
};

const ifNotAuthenticated = (to, from, next) => {
    console.log("ifNotAuthenticated");
    console.log("Auth.loggedId: ", Auth.loggedIn);
    if (!Auth.loggedIn)
    {
        next();
        return
    }
    // if (!document.cookie)
    // {
    //     next();
    //     return
    // }
    next('/')
};

export default [
    { path: '/register', component: Register, beforeEnter: ifNotAuthenticated},
    { path: '/login', component: Login, beforeEnter: ifNotAuthenticated},
    { path: '/my_profile', component: MyProfile, beforeEnter: ifAuthenticated, props: {user_id: true}},
    { path: '/my_profile/:user_id', component: MyProfile, beforeEnter: ifAuthenticated},
    { path: '/forgot_password', component: ForgotPassword, beforeEnter: ifNotAuthenticated},
    { path: '/users', component: UsersList, beforeEnter: ifAuthenticated},
    { path: '/users/:id', component: ViewProfile, beforeEnter: ifAuthenticated},
    { path: '/view_profile', component: ViewProfile, beforeEnter: ifAuthenticated}, // This can be deleted
    { path: '/', component: Home},
    { path: '/home', component: Home},
    // { path: '/my_profile/settings', component: Settings},
    // { path: '/my_profile/about_me', component: AboutMe},
    // { path: '/header', component: Header}
]
