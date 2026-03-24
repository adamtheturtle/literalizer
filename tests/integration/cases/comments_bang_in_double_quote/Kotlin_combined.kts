fun _declaration() {
    val my_data = mapOf<String, String>(
        "key" to "\"bang!\"",  // real
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, String>(
        "key" to "\"bang!\"",  // real
    )
}
