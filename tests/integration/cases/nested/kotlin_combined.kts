fun _declaration() {
    val my_data = mapOf<String, Any?>(
        "users" to listOf<Any?>(mapOf<String, Any?>("name" to "Bob", "tags" to listOf<Any?>("admin", "user")), mapOf<String, Any?>("name" to "Carol", "tags" to listOf<Any?>("guest"))),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, Any?>(
        "users" to listOf<Any?>(mapOf<String, Any?>("name" to "Bob", "tags" to listOf<Any?>("admin", "user")), mapOf<String, Any?>("name" to "Carol", "tags" to listOf<Any?>("guest"))),
    )
}
