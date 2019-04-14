package cf.coffeebreak42.service

import cf.coffeebreak42.model.NewUser
import cf.coffeebreak42.model.User
import java.sql.ResultSet

class UserService {

    suspend fun getAllUsers(): List<User> {
        val result = DatabaseFactory.dbQuery("SELECT * FROM User")
        val users = ArrayList<User>()
        if (result != null) {
            while (result.next()) {
                users.add(toUser(result))
            }
        }
        return users
    }

    suspend fun getUser(userId: Int): User? {
        val result = DatabaseFactory.dbQuery("SELECT * FROM User WHERE User.userId = ?")
        {
            it.setInt(1, userId)
        }

        if (result != null) {
            if (result.first())
                return User(userId, result.getString("email"))
        }
        return null
    }

    fun addUser(user: NewUser): User {
        val result = DatabaseFactory.dbUpdate("INSERT INTO Users VALUES (?, ?)")
        {

        }
    }

    fun createTable() {
        DatabaseFactory.dbUpdate("""
            |CREATE TABLE User(
            |userId numeric,
            |email varchar(20)
            |);""".trimMargin())
    }

    private fun toUser(row: ResultSet) = User(
        userId = row.getInt("userId"),
        email = row.getString("email")
    )
}