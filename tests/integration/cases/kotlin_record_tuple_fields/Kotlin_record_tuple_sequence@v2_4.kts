data class Record0(val pair: Pair<Int, Int>, val mixed: Pair<Int, String>, val triple: Triple<Int, String, Boolean>, val nested: Pair<Pair<Int, String>, Triple<Int, Boolean, Double>>, val empty: List<Any?>, val single: List<Any?>, val long: List<Any?>)
val my_data = Record0(
    pair = Pair(
        1,
        2,
    ),
    mixed = Pair(
        1,
        "text",
    ),
    triple = Triple(
        1,
        "text",
        true,
    ),
    nested = Pair(
        Pair(
            1,
            "text",
        ),
        Triple(
            2,
            false,
            3.5,
        ),
    ),
    empty = listOf<Any?>(),
    single = listOf<Any?>(
        1,
    ),
    long = listOf<Any?>(
        1,
        2,
        3,
        4,
    ),
)
