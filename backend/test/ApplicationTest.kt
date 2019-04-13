package cf.coffeebreak42

import com.google.gson.Gson
import io.ktor.http.HttpMethod
import io.ktor.http.HttpStatusCode
import io.ktor.server.testing.handleRequest
import io.ktor.server.testing.setBody
import io.ktor.server.testing.withTestApplication
import java.util.*
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.fail


data class Snippets(val snippets: MutableList<Snippet>)

class ApplicationTest {

    private val json = "application/json"
    private val gson = Gson()

    @Test
    fun testRoot() {
        withTestApplication({ module(testing = true) }) {
            handleRequest(HttpMethod.Get, "/").apply {
                assertEquals(HttpStatusCode.OK, response.status())
                assertEquals("HELLO WORLD!", response.content)
            }
        }
    }

    @Test
    fun testSnippets() {
        withTestApplication({ module(testing = true)}) {
            val uuid = UUID.randomUUID()
            val testSnippet = Snippet(text = uuid.toString())
            val content = gson.toJson(mapOf("snippet" to testSnippet))
            val createRequest = handleRequest(HttpMethod.Post, "/snippets") {
                setBody(content)
                addHeader("Content-Type", json)
            }
            with (createRequest) {
                assertEquals(HttpStatusCode.OK, response.status())
            }
            handleRequest(HttpMethod.Get, "/snippets").apply {
                assertEquals(HttpStatusCode.OK, response.status())
                val snippets = gson.fromJson(response.content, Snippets::class.java)
                snippets.snippets.find { it == testSnippet } ?: fail("Snippet not found")
            }
        }
    }
}
