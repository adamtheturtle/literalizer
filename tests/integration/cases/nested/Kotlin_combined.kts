fun _declaration() {
    val my_data = mapOf<String, Any?>(
        "users" to listOf<Any?>(mapOf<String, Any?>("name" to "Bob", "tags" to arrayOf("admin", "user")), mapOf<String, Any?>("name" to "Carol", "tags" to arrayOf("guest"))),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, Any?>(
        "users" to listOf<Any?>(mapOf<String, Any?>("name" to "Bob", "tags" to arrayOf("admin", "user")), mapOf<String, Any?>("name" to "Carol", "tags" to arrayOf("guest"))),
    )
}
