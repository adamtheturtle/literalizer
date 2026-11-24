data class Record0(val numbers: Pair<Int, Int>, val nested_numbers: Pair<Pair<Int, Int>, Pair<Int, Int>>, val words: List<Any?>, val flag: Boolean)
val my_data = Record0(
    numbers = Pair(
        1,
        2,
    ),
    nested_numbers = Pair(
        Pair(
            3,
            4,
        ),
        Pair(
            5,
            6,
        ),
    ),
    words = listOf<Any?>(
        "s",
    ),
    flag = true,
)
