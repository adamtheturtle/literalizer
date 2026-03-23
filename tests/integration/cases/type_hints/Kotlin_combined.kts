import java.time.LocalDate
import java.time.LocalDateTime
fun _declaration() {
    val my_data = mapOf<String, Any?>(
        "name" to "Alice",
        "age" to 30,
        "active" to true,
        "score" to null,
        "joined" to LocalDate.of(2024, 1, 15),
        "last_login" to LocalDateTime.of(2024, 1, 15, 12, 30, 0),
        "avatar" to "48656c6c6f",
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, Any?>(
        "name" to "Alice",
        "age" to 30,
        "active" to true,
        "score" to null,
        "joined" to LocalDate.of(2024, 1, 15),
        "last_login" to LocalDateTime.of(2024, 1, 15, 12, 30, 0),
        "avatar" to "48656c6c6f",
    )
}
