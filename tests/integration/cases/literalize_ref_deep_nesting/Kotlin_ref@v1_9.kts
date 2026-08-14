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
val my_data = mapOf<String, Map<String, Map<String, Array<Array<Int>>>>>(
    "a" to mapOf<String, Map<String, Array<Array<Int>>>>(
        "b" to mapOf<String, Array<Array<Int>>>(
            "c" to deep,
        ),
    ),
)
