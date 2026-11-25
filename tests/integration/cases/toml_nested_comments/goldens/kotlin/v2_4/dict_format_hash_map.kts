val my_data = hashMapOf<String, Any?>(
    // About the first dotted key.
    // About the second dotted key.
    "dotted" to hashMapOf<String, Int>("first" to 1, "second" to 2),
    "plain" to 3,  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    "entries" to listOf<Map<String, String>>(hashMapOf<String, String>("name" to "one"), hashMapOf<String, String>("name" to "two")),
    // Inside the table.
    "table" to hashMapOf<String, Int>("inner" to 4),
)
