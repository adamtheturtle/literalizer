import java.time.LocalDate
import java.time.LocalDateTime
fun _declaration() {
    val my_data = listOf<Any?>(
        LocalDateTime.of(2024, 1, 15, 12, 30, 0),
        LocalDateTime.of(2024, 6, 30, 8, 0, 0),
        LocalDateTime.of(2024, 12, 25, 18, 45, 0),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = listOf<Any?>(
        LocalDateTime.of(2024, 1, 15, 12, 30, 0),
        LocalDateTime.of(2024, 6, 30, 8, 0, 0),
        LocalDateTime.of(2024, 12, 25, 18, 45, 0),
    )
}
