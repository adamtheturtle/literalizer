data class Record0(val value: IntArray)
val shared = Record0(
    value = intArrayOf(
        1,
        2,
    ),
)
val my_data = listOf<Record0>(
    shared,
    shared,
)
