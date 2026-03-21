import java.time.LocalDate
fun _declaration() {
    val my_data = listOf<Any?>(
        LocalDate.of(2024, 1, 15),
        LocalDate.of(2024, 6, 30),
        LocalDate.of(2024, 12, 25),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = listOf<Any?>(
        LocalDate.of(2024, 1, 15),
        LocalDate.of(2024, 6, 30),
        LocalDate.of(2024, 12, 25),
    )
}
