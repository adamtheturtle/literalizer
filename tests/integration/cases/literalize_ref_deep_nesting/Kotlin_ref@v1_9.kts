val deep = arrayOf(
    arrayOf(
        "one",
        "two",
    ),
    arrayOf(
        "three",
        "four",
    ),
)
val my_data = mapOf<String, Map<String, Map<String, Array<Array<String>>>>>(
    "a" to mapOf<String, Map<String, Array<Array<String>>>>(
        "b" to mapOf<String, Array<Array<String>>>(
            "c" to deep,
        ),
    ),
)
