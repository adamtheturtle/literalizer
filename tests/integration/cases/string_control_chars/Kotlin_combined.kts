fun _declaration() {
    val my_data = arrayOf(
        "line1\r\nline2",
        "line1\rline2",
        "",
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = arrayOf(
        "line1\r\nline2",
        "line1\rline2",
        "",
    )
}
