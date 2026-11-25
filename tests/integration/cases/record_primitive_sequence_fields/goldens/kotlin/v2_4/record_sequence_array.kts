data class Record0(val flags: Array<Any?>, val values: Array<Any?>, val ints: Array<Any?>, val text: Array<Any?>, val nested_flags: Array<Any?>, val nested_values: Array<Any?>)
val my_data = Record0(
    flags = arrayOf<Any?>(
        true,
        false,
    ),
    values = arrayOf<Any?>(
        1.5,
        -2.25,
    ),
    ints = arrayOf<Any?>(
        1,
        2,
    ),
    text = arrayOf<Any?>(
        "a",
    ),
    nested_flags = arrayOf<Any?>(
        arrayOf<Any?>(
            true,
        ),
        arrayOf<Any?>(
            false,
        ),
    ),
    nested_values = arrayOf<Any?>(
        arrayOf<Any?>(
            1.5,
        ),
        arrayOf<Any?>(
            2.25,
        ),
    ),
)
