val my_data = mapOf<String, Any?>(
    "flow" to intArrayOf(
        1,
        // After the first element.
        2,
    ),
    // Between the key and its value.
    "gap" to 3,
    // On the block scalar header.
    "block" to "Text.\n",
    "nested" to intArrayOf(
        1,
        1,
        // On the nested alias.
    ),
    "anchored" to 4,
    "alias" to 4,
    // On the alias.
)
