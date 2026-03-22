fun _declaration() {
    val my_data = listOf<Any?>(
        mapOf<String, Any?>("key" to "hello   world", "value" to 1),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = listOf<Any?>(
        mapOf<String, Any?>("key" to "hello   world", "value" to 1),
    )
}
