val deep = arrayOf(
    intArrayOf(
        1,
        2,
    ),
    intArrayOf(
        3,
        4,
    ),
)
val my_data = mapOf<String, Map<String, Map<String, Map<String, String>>>>(
    "a" to mapOf<String, Map<String, Map<String, String>>>(
        "b" to mapOf<String, Map<String, String>>(
            "c" to deep,
        ),
    ),
)
