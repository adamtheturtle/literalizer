fun _declaration() {
    val my_data = listOf<Any?>(
        mapOf<String, Any?>("name" to "Alice", "age" to 30),
        mapOf<String, Any?>("name" to "Bob", "age" to 25),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = listOf<Any?>(
        mapOf<String, Any?>("name" to "Alice", "age" to 30),
        mapOf<String, Any?>("name" to "Bob", "age" to 25),
    )
}
