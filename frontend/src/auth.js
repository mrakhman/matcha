export let Auth = {
    loggedIn: false, // I changed it to true!!!!!!!!!!!!!!!!
    login: function() {this.loggedIn = true},
    logout: function() {this.loggedIn = false}
    // change: function() {this.loggedIn = !this.loggedIn}
};
