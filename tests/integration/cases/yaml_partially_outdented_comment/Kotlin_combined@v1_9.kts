var my_data = mapOf<String, Any?>(
    "a" to mapOf<String, Any?>(
        "b" to intArrayOf(1),
        // Outdented from the sequence, so the inner mapping claims this.
        "c" to 2,
    ),
    // Outdented from the inner mapping too, so the root claims this.
    "d" to 3,
)
my_data = mapOf<String, Any?>(
    "a" to mapOf<String, Any?>(
        "b" to intArrayOf(1),
        // Outdented from the sequence, so the inner mapping claims this.
        "c" to 2,
    ),
    // Outdented from the inner mapping too, so the root claims this.
    "d" to 3,
)
