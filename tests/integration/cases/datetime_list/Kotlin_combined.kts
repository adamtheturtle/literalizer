import java.time.LocalDateTime
fun _declaration() {
    val my_data = arrayOf(
        LocalDateTime.of(2024, 1, 15, 12, 30, 0),
        LocalDateTime.of(2024, 6, 1, 8, 0, 0),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = arrayOf(
        LocalDateTime.of(2024, 1, 15, 12, 30, 0),
        LocalDateTime.of(2024, 6, 1, 8, 0, 0),
    )
}
