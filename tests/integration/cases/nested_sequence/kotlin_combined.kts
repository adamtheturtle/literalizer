fun _declaration() {
    val my_data = listOf<Any?>(
        true,
        "hi",
        intArrayOf(1, 2),
        null,
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = listOf<Any?>(
        true,
        "hi",
        intArrayOf(1, 2),
        null,
    )
}
