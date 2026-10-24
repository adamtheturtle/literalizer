data class Record1(val values: Array<Any?>)
data class Record2(val nested: Array<Any?>)
data class Record0(val trivial: Record1, val nested: Record2)
val trivial = Record1(
    values = arrayOf<Any?>(
        1,
        2,
    ),
)
val nested = Record2(
    nested = arrayOf<Any?>(
        arrayOf<Any?>(
            1,
            2,
        ),
        arrayOf<Any?>(
            3,
            4,
        ),
    ),
)
val my_data = Record0(
    trivial = trivial,
    nested = nested,
)
