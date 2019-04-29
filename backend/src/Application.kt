package cf.coffeebreak42

import cf.coffeebreak42.model.NewUser
import cf.coffeebreak42.service.DatabaseFactory
import cf.coffeebreak42.service.UserService
import com.fasterxml.jackson.databind.SerializationFeature
import com.fasterxml.jackson.databind.exc.MismatchedInputException
import com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException
import io.ktor.application.Application
import io.ktor.application.call
import io.ktor.application.install
import io.ktor.auth.Authentication
import io.ktor.features.CORS
import io.ktor.features.ContentNegotiation
import io.ktor.http.ContentType
import io.ktor.http.HttpHeaders
import io.ktor.http.HttpMethod
import io.ktor.jackson.jackson
import io.ktor.request.receive
import io.ktor.response.respond
import io.ktor.response.respondText
import io.ktor.routing.get
import io.ktor.routing.post
import io.ktor.routing.route
import io.ktor.routing.routing
import java.util.*

fun main(args: Array<String>): Unit = io.ktor.server.netty.EngineMain.main(args)

//fun main() = myTest()
//
//inline fun foo(arg1: Any, arg2: Int = 2, inline: (Int) -> Unit) {
//    println("$arg1 $arg2")
//    if (arg1 is Int)
//        inline(arg1)
//}
//
//fun myTest() {
//    foo(1) {println("from inside: $it")}
//    foo(arg1 = 5, arg2 = 2) {println("from inside")}
//}


data class Snippet(val text: String)

data class PostSnippet(val snippet: Text) {
    data class Text(val text: String)
}

val snippets: MutableList<Snippet> = Collections.synchronizedList(mutableListOf(
    Snippet("hello"),
    Snippet("world")
))

@Suppress("unused") // Referenced in application.conf
@kotlin.jvm.JvmOverloads
fun Application.module(testing: Boolean = false) {
    install(CORS) {
        method(HttpMethod.Options)
        method(HttpMethod.Put)
        method(HttpMethod.Delete)
        method(HttpMethod.Patch)
        header(HttpHeaders.Authorization)
        header("MyCustomHeader")
        allowCredentials = true
        anyHost() // @TODO: Don't do this in production if possible. Try to limit it.
    }

    install(Authentication) {
    }

    install(ContentNegotiation) {
        jackson {
            enable(SerializationFeature.INDENT_OUTPUT)
        }
    }

    DatabaseFactory.init(testing)

    val userService = UserService()

    userService.createTable()
    userService.addUser(NewUser("test@test.xyz"))
    userService.addUser(NewUser("test2@emample.com"))
    userService.addUser(NewUser("masha@emample.com"))


    routing {
        get("/") {
            call.respondText("HELLO WORLD!", contentType = ContentType.Text.Plain)
        }

        get("/json") {
            call.respond(mapOf("hello" to "world"))
        }

        route("/snippets") {
            get {
                call.respond(mapOf("snippets" to synchronized(snippets) { snippets.toList() }))
                println("GET snippets")
            }

            post {
                val post = call.receive<PostSnippet>()
                snippets += Snippet(post.snippet.text)
                call.respond(mapOf("OK" to true))
            }
        }

        route("/users") {
            get("/") {
                call.respond(mapOf("users" to userService.getAllUsers()))
            }
            post("/") {
                val post = try {
                    call.receive<NewUser>()
                } catch (e: MissingKotlinParameterException) {
                    null
                } catch (e: MismatchedInputException) {
                    null
                }
                if (post != null) {
                    val user = userService.addUser(post)
                    if (user != null)
                        call.respond(mapOf("user" to user))
                    else
                        call.respond("Error")
                }
                else
                    call.respond("Error")
            }
            get("/{userId}") {
                val userId = call.parameters["userID"]?.toIntOrNull()
                if (userId != null)
                    call.respond(mapOf("user" to userService.getUser(userId)))
                else
                    call.respond("Error")
            }
        }
    }
}

