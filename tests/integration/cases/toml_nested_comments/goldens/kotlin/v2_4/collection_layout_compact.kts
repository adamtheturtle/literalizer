val my_data = mapOf<String, Any?>(
    // About the first dotted key.
    // About the second dotted key.
    "dotted" to mapOf<String, Int>("first" to 1, "second" to 2),
    "plain" to 3,  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    "entries" to listOf<Map<String, String>>(mapOf<String, String>("name" to "one"), mapOf<String, String>("name" to "two")),
    // Inside the table.
    "table" to mapOf<String, Int>("inner" to 4),
)
