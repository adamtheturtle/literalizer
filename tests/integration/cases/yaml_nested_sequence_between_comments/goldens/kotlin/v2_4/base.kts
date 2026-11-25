val my_data = listOf<Any?>(
    listOf<Any?>(
        mapOf<String, String>("item" to "existing"),
        "kept",
        // This comment trails the first pair.
    ),
    listOf<Any?>(mapOf<String, String>("item" to "next"), "also kept"),
    // This comment describes the last pair.
    listOf<Any?>(mapOf<String, String>("item" to "last"), "kept too"),
)
