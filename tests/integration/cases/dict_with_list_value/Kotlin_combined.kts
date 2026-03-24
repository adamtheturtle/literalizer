fun _declaration() {
    val my_data = mapOf<String, Any?>(
        "name" to "Alice",
        "scores" to intArrayOf(10, 20, 30),
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, Any?>(
        "name" to "Alice",
        "scores" to intArrayOf(10, 20, 30),
    )
}
