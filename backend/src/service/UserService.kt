package cf.coffeebreak42.service

import cf.coffeebreak42.model.NewUser
import cf.coffeebreak42.model.User
import java.sql.ResultSet

class UserService {
    private val dbName = "User"

    fun getAllUsers(): List<User> {
        val result = DatabaseFactory.dbQuery("SELECT * FROM $dbName")
        val users = ArrayList<User>()
        if (result != null) {
            while (result.next()) {
                users.add(toUser(result))
            }
        }
        return users
    }

    fun getUser(userId: Int): User? {
        val result = DatabaseFactory.dbQuery("SELECT * FROM $dbName WHERE User.userId = ?")
        {
            it.setInt(1, userId)
        }

        if (result != null) {
            if (result.first())
                return User(userId, result.getString("email"))
        }
        return null
    }

    fun addUser(user: NewUser): User? {
        val result = DatabaseFactory.dbInsert("INSERT INTO $dbName (email) VALUES (?)", {
//            it.setInt(1, user.userId!!) // @TODO: Alarm!
            it.setString(1, user.email)
        })
        if (result != null)
            return User(result, user.email)
        return null
    }

    fun createTable() {
        DatabaseFactory.dbUpdate("""
            |CREATE TABLE $dbName(
            |userId SERIAL PRIMARY KEY,
            |email varchar(20)
            |);""".trimMargin())
    }

    private fun toUser(row: ResultSet) = User(
        userId = row.getInt("userId"),
        email = row.getString("email")
    )
}