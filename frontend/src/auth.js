export let Auth = {
    loggedIn: false,
    login: function() {this.loggedIn = true},
    logout: function() {this.loggedIn = false},
    change: function() {this.loggedIn = !this.loggedIn}
};