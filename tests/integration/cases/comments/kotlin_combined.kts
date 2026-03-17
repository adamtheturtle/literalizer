fun _declaration() {
    val my_data = mapOf<String, Any?>(
        // Server configuration
        "host" to "localhost",  // default host
        "port" to 8080,
        // Enable debug mode
        "debug" to true,
    )
}
fun _assignment() {
    var my_data: Any? = null
    my_data = mapOf<String, Any?>(
        // Server configuration
        "host" to "localhost",  // default host
        "port" to 8080,
        // Enable debug mode
        "debug" to true,
    )
}
