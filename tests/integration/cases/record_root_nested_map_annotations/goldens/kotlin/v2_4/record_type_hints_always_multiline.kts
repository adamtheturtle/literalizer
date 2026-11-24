data class Record0(val x: Int)
val my_data: LinkedHashMap<String, Any?> = linkedMapOf<String, Any?>(
    "outer" to listOf<Any?>(
        linkedMapOf<String, Any?>(
            "inner" to Record0(
                x = 1,
            ),
        ),
        linkedMapOf<String, Any?>(
            "inner" to Record0(
                x = 2,
            ),
        ),
    ),
)
