data class Record0(val flags: BooleanArray, val values: DoubleArray, val ints: IntArray, val text: Array<String>, val nested_flags: Array<BooleanArray>, val nested_values: Array<DoubleArray>)
val my_data = Record0(
    flags = booleanArrayOf(
        true,
        false,
    ),
    values = doubleArrayOf(
        1.5,
        -2.25,
    ),
    ints = intArrayOf(
        1,
        2,
    ),
    text = arrayOf(
        "a",
    ),
    nested_flags = arrayOf(
        booleanArrayOf(
            true,
        ),
        booleanArrayOf(
            false,
        ),
    ),
    nested_values = arrayOf(
        doubleArrayOf(
            1.5,
        ),
        doubleArrayOf(
            2.25,
        ),
    ),
)
