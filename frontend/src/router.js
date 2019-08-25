import MyProfile from './components/MyProfile.vue';
import Register from "./components/Register";
import ViewProfile from "./components/ViewProfile";
import ForgotPassword from "./components/ForgotPassword";
import UsersList from "./components/UsersList";
import Login from "./components/Login";
import Home from "./components/Home";
import NotFound from "./components/NotFound";
import Notifications from "./components/Notifications";
import Chat from "./components/Chat";
import Activation from "./components/Activation";
import ResetPassword from "./components/ResetPassword";
import SetNewEmail from "./components/SetNewEmail";
import History from "./components/History";
import ChatList from "./components/ChatList";

import store from './store';

// We can just register the array [{}, {}] in main.js inside "const router = new VueRouter({ ..."
// without creating a separate file router.js

const ifAuthenticated = (to, from, next) => {
    if (store.state.logged_in)
    {
        next();
        return
    }
    next('/login')
};

const ifNotAuthenticated = (to, from, next) => {
    if (!store.state.logged_in)
    {
        next();
        return
    }
    next('/')
};

const canSearch = (to, from, next) => {
    if (store.state.logged_in && store.state.user && store.state.user.dob && store.state.user.gender)
    {
        next();
        return
    }
    next('/')
};

export default [
    { path: '/register', component: Register, beforeEnter: ifNotAuthenticated},
    { path: '/login', component: Login, beforeEnter: ifNotAuthenticated},
    { path: '/my_profile', component: MyProfile, beforeEnter: ifAuthenticated, meta: {auth: true}},
    { path: '/forgot_password', component: ForgotPassword, beforeEnter: ifNotAuthenticated},
    { path: '/search/', component: UsersList, beforeEnter: canSearch, meta: {auth: true}},
    { path: '/search/:page_n', component: UsersList, beforeEnter: canSearch, meta: {auth: true}},
    { path: '/users/:id', component: ViewProfile, beforeEnter: ifAuthenticated, meta: {auth: true}},
    { path: '/', component: Home, beforeEnter: ifAuthenticated, meta: {auth: true}},
    { path: '/home', component: Home, beforeEnter: ifAuthenticated, meta: {auth: true}},
    { path: '/chat', component: ChatList, beforeEnter: ifAuthenticated, meta: {auth: true}},
    { path: '/chat/:id', component: Chat, beforeEnter: ifAuthenticated, meta: {auth: true}},
    { path: '/notifications', component: Notifications, beforeEnter: ifAuthenticated, meta: {auth: true}},
    { path: '/activation/:token', component: Activation, beforeEnter: ifNotAuthenticated},
    { path: '/activation/resend', component: Activation, beforeEnter: ifNotAuthenticated},
    { path: '/reset_password/:token', component: ResetPassword, beforeEnter: ifNotAuthenticated},
    { path: '/activate_email/:token', component: SetNewEmail},
    { path: '/history', component: History, beforeEnter: ifAuthenticated, meta: {auth: true}},
    { path: '*', component: NotFound},
]
