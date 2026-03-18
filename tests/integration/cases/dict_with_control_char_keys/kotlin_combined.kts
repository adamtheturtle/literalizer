fun _declaration() {
    val my_data = mapOf<String, Any?>(
        "key\nwith\nnewlines" to "value1",
        "key	with	tabs" to "value2",
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, Any?>(
        "key\nwith\nnewlines" to "value1",
        "key	with	tabs" to "value2",
    )
}
