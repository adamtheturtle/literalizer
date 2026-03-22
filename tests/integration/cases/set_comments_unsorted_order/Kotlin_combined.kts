fun _declaration() {
    val my_data = setOf<Any?>(
        // before apple
        "apple",
        "banana",  // banana inline
        // trailing
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = setOf<Any?>(
        // before apple
        "apple",
        "banana",  // banana inline
        // trailing
    )
}
