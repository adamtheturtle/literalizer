fun _declaration() {
    val my_data = mapOf<String, Any?>(
        "a" to mapOf<String, Int>("x" to 1),
        "b" to 2,
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, Any?>(
        "a" to mapOf<String, Int>("x" to 1),
        "b" to 2,
    )
}
