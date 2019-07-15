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
// import {Auth} from './auth'
import Home from "./components/Home";
import NotFound from "./components/NotFound";
import Notifications from "./components/Notifications";
import Chat from "./components/Chat";
import Activation from "./components/Activation";
import ResetPassword from "./components/ResetPassword";
import SetNewEmail from "./components/SetNewEmail";
import History from "./components/History";

// We can just register the array [{}, {}] in main.js inside "const router = new VueRouter({ ..."
// without creating a separate file router.js

const ifAuthenticated = (to, from, next) => {
    if (localStorage.getItem('user_id'))
    {
        next();
        return
    }
    next('/login')
};

const ifNotAuthenticated = (to, from, next) => {
    if (!localStorage.getItem('user_id'))
    {
        next();
        return
    }
    next('/')
};

export default [
    { path: '/register', component: Register, beforeEnter: ifNotAuthenticated},
    { path: '/login', component: Login, beforeEnter: ifNotAuthenticated},
    { path: '/my_profile', component: MyProfile, beforeEnter: ifAuthenticated},
    // { path: '/my_profile/:user_id', component: MyProfile, beforeEnter: ifAuthenticated},
    { path: '/forgot_password', component: ForgotPassword, beforeEnter: ifNotAuthenticated},
    { path: '/search/', component: UsersList, beforeEnter: ifAuthenticated}, // kuku
    { path: '/search/:page_n', component: UsersList, beforeEnter: ifAuthenticated}, // kuku
    { path: '/users/:id', component: ViewProfile, beforeEnter: ifAuthenticated},
    { path: '/', component: Home, beforeEnter: ifAuthenticated},
    { path: '/home', component: Home, beforeEnter: ifAuthenticated},
    { path: '/chat', component: Chat, beforeEnter: ifAuthenticated},
    { path: '/notifications', component: Notifications, beforeEnter: ifAuthenticated},
    { path: '/activation/:token', component: Activation, beforeEnter: ifNotAuthenticated},
    { path: '/reset_password/:token', component: ResetPassword, beforeEnter: ifNotAuthenticated},
    { path: '/new_email/:token', component: SetNewEmail},
    { path: '/history', component: History, beforeEnter: ifAuthenticated},
    { path: '*', component: NotFound},

// { path: '/view_profile', component: ViewProfile, beforeEnter: ifAuthenticated}, // This can be deleted
// { path: '/my_profile/settings', component: Settings},
// { path: '/my_profile/about_me', component: AboutMe},
// { path: '/header', component: Header}
]
