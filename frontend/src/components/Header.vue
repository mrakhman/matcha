<template>
    <div id="header">
        <b-navbar toggleable="lg" variant="light">
            <a href="/"><img alt="Time Club logo" src="../assets/timeclub-logo_orange.png" width="40"></a>
            <h1 class="header_text"> <a href="/"> Matcha </a></h1>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item-dropdown text="My profile" left>
                        <b-dropdown-item href="/my_profile">About me</b-dropdown-item>
                        <b-dropdown-item href="/my_profile">Settings</b-dropdown-item>
                    </b-nav-item-dropdown>
<!--                    <b-nav-item href="#">My profile</b-nav-item>-->
                    <b-nav-item href="/my_profile">My profile</b-nav-item>
                    <b-nav-item href="#" disabled>Disabled</b-nav-item>
                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
<!--                    <b-nav-form>-->
<!--                        <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>-->
<!--                        <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>-->
<!--                    </b-nav-form>-->


<!--                    <b-nav-item-dropdown right>-->
<!--                        &lt;!&ndash; Using 'button-content' slot &ndash;&gt;-->
<!--                        <template slot="button-content">User</template>-->
<!--                        <b-dropdown-item href="#">Profile</b-dropdown-item>-->
<!--                        <b-dropdown-item href="#">Sign Out</b-dropdown-item>-->
<!--                    </b-nav-item-dropdown>-->
                    <b-form inline>
                        <b-form-input id="inline-form-input-name" class="mb-2 mr-sm-2 mb-sm-0" placeholder="Username"></b-form-input>
                        <label class="sr-only" for="inline-form-input-password">Password</label>
                        <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
                            <b-form-input type="password" id="inline-form-input-password" placeholder="Password"></b-form-input>
                        </b-input-group>

                        <b-button type="submit" variant="outline-primary" size="sm">Login</b-button>
                    </b-form>
                    <b-nav-item href="#"><font size="-1">Forgot password</font></b-nav-item>
                    <b-form inline>
                        <b-button type="submit" variant="outline-primary" size="sm">Logout</b-button>
                    </b-form>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
<!--        <hr>-->
    </div>

<!--    <div id="header">-->
<!--        <b-nav id="menu" >-->
<!--            <div class="header_flex_start">-->
<!--                <img alt="Time Club logo" src="../assets/timeclub-logo_orange.png">-->
<!--                <h1 class="header_text"> Matcha </h1>-->
<!--                <b-nav-item active>Active</b-nav-item>-->
<!--                <b-nav-item>Link</b-nav-item>-->
<!--                <b-nav-item>Logout</b-nav-item>-->
<!--            <div class="header_flex_end">-->
<!--                <b-button variant="mygreen">Login</b-button>-->
<!--            </div>-->
<!--            </div>-->
<!--        </b-nav>-->
<!--        <hr>-->
<!--    </div>-->

</template>

<script>
    export default {
        name: "Header.vue"
    }
</script>

<style scoped lang="scss">
    @import '../assets/_custom.scss';
    @import '~bootstrap/scss/bootstrap.scss';
    @import '~bootstrap-vue/src/index.scss';

    #header {
        background-color: #f8f9fa;
        padding: 5px;
    }

    #menu {
        width: 100%;
    }

    .header_text {
        color: black;
        font-size: 24px;
        margin: 5px;
        font-weight: lighter;
    }

    .header_text a {
        color: black;
        text-decoration: none;
    }

    .header_text a:hover {
        color: #396;
    }

    .header_flex_start {
        /*margin-bottom: 10px;*/
        width: 100%;
        text-align: left;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
    }

    .header_flex_end {
        /*text-align: left;*/
        display: flex;
        /*flex-direction: row;*/
        justify-content: flex-end;
    }

    .header_flex_start > img {
        width: 40px;
        height: 40px;
    }


</style>

