fun _declaration() {
    val my_data = mapOf<String, Any?>(
        "date" to LocalDate.of(2024, 1, 15),
        "datetime" to LocalDateTime.of(2024, 1, 15, 12, 30, 0),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, Any?>(
        "date" to LocalDate.of(2024, 1, 15),
        "datetime" to LocalDateTime.of(2024, 1, 15, 12, 30, 0),
    )
}
