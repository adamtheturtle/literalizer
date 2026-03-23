fun _declaration() {
    val my_data = mapOf<String, String>(
        "key" to "value \" # not a comment",  // real
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, String>(
        "key" to "value \" # not a comment",  // real
    )
}
