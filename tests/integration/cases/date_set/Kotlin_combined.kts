import java.time.LocalDate
fun _declaration() {
    val my_data = setOf<LocalDate>(
        LocalDate.of(2024, 1, 15),
        LocalDate.of(2024, 6, 1),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = setOf<LocalDate>(
        LocalDate.of(2024, 1, 15),
        LocalDate.of(2024, 6, 1),
    )
}
