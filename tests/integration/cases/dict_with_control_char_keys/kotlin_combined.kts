fun _declaration() {
    val my_data = mapOf<String, String>(
        "key\nwith\nnewlines" to "value1",
        "key\twith\ttabs" to "value2",
        "" to "value3",
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, String>(
        "key\nwith\nnewlines" to "value1",
        "key\twith\ttabs" to "value2",
        "" to "value3",
    )
}
