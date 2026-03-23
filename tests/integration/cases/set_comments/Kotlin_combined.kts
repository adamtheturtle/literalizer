fun _declaration() {
    val my_data = setOf<String>(
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = setOf<String>(
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    )
}
