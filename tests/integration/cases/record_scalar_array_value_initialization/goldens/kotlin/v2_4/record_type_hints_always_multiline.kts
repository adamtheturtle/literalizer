data class Record0(val numbers: IntArray, val nested_numbers: Array<IntArray>, val words: Array<String>, val flag: Boolean)
val my_data: Record0 = Record0(
    numbers = intArrayOf(
        1,
        2,
    ),
    nested_numbers = arrayOf(
        intArrayOf(
            3,
            4,
        ),
        intArrayOf(
            5,
            6,
        ),
    ),
    words = arrayOf(
        "s",
    ),
    flag = true,
)
