package cf.coffeebreak42.model


data class User(val userId: Int, val email: String)
data class NewUser(val userId: Int?, val email: String)
