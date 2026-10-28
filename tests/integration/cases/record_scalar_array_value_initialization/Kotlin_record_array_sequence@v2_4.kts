data class Record0(val numbers: Array<Any?>, val nested_numbers: Array<Any?>, val words: Array<Any?>, val flag: Boolean)
val my_data = Record0(
    numbers = arrayOf<Any?>(
        1,
        2,
    ),
    nested_numbers = arrayOf<Any?>(
        arrayOf<Any?>(
            3,
            4,
        ),
        arrayOf<Any?>(
            5,
            6,
        ),
    ),
    words = arrayOf<Any?>(
        "s",
    ),
    flag = true,
)
