data class Record0(val flags: Pair<Boolean, Boolean>, val values: Pair<Double, Double>, val ints: Pair<Int, Int>, val text: List<Any?>, val nested_flags: Pair<List<Any?>, List<Any?>>, val nested_values: Pair<List<Any?>, List<Any?>>)
val my_data = Record0(
    flags = Pair(
        true,
        false,
    ),
    values = Pair(
        1.5,
        -2.25,
    ),
    ints = Pair(
        1,
        2,
    ),
    text = listOf<Any?>(
        "a",
    ),
    nested_flags = Pair(
        listOf<Any?>(
            true,
        ),
        listOf<Any?>(
            false,
        ),
    ),
    nested_values = Pair(
        listOf<Any?>(
            1.5,
        ),
        listOf<Any?>(
            2.25,
        ),
    ),
)
