package cf.coffeebreak42.service

import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import java.sql.Connection
import java.sql.PreparedStatement
import java.sql.ResultSet

object DatabaseFactory {
    private lateinit var connection: Connection

    fun init(testing: Boolean = false) {
        val driverClassName:String
        val jdbcUrl:String
        if (!testing) {
            driverClassName = "org.h2.Driver" // @TODO: Update
            jdbcUrl = "jdbc:h2:mem:test"
        }
        else {
            driverClassName = "org.h2.Driver"
            jdbcUrl = "jdbc:h2:mem:test"
        }
        this.connection = hikari(driverClassName, jdbcUrl).connection
    }

    private fun hikari(driverClassName: String, jdbcUrl: String): HikariDataSource {
        val config = HikariConfig()
        config.driverClassName = driverClassName
        config.jdbcUrl = jdbcUrl
        config.maximumPoolSize = 3
        config.isAutoCommit = false
        config.transactionIsolation = "TRANSACTION_REPEATABLE_READ"
        config.validate()
        return HikariDataSource(config)
    }

//    suspend fun <T> dbQuery(query:String): List<T> = withContext(Dispatchers.IO) {
//        val pst = connection.prepareStatement(query)
//        val result = pst.executeQuery()
//        var objs: List<T>? = null
//        objs = ArrayList()
//        var obj: T?
//        while (result.next()) {
//
//
//        }
//        return objs
//    }

    fun dbQuery(query: String, prepare: ((PreparedStatement) -> Unit)? = null): ResultSet? {
        val pst = connection.prepareStatement(query)
        if (pst != null) {
            if (prepare != null)
                prepare(pst)
            return pst.executeQuery()
        }
        return null
    }

    // If inserted many -> returns only first id!
    fun dbInsert(query: String, prepare: ((PreparedStatement) -> Unit)? = null, columnIndex: Int = 1): Int? {
        val pst = connection.prepareStatement(query)
        if (pst != null) {
            if (prepare != null)
                prepare(pst)
            pst.execute()
            val rs = pst.generatedKeys
            if (rs.next())
                return rs.getInt(columnIndex)
        }
        return null
    }

    fun dbUpdate(query: String, prepare: ((PreparedStatement) -> Unit)? = null): Boolean {
        val pst = connection.prepareStatement(query)
        if (pst != null) {
            if (prepare != null)
                prepare(pst)
            return pst.execute()
        }
        return false
    }
}