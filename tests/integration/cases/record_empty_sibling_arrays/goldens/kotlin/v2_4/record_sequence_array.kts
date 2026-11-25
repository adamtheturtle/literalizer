data class Record1(val item: Int)
data class Record2(val item: Any?)
data class Record0(val integers: Array<Any?>, val nulls: Array<Any?>, val nested: Array<Any?>, val reversed: Array<Any?>)
val my_data = Record0(
    integers = arrayOf<Any?>(
        listOf<Record1>(),
        listOf<Record1>(
            Record1(
                item = 1,
            ),
        ),
    ),
    nulls = arrayOf<Any?>(
        listOf<Record2>(),
        listOf<Record2>(
            Record2(
                item = null,
            ),
        ),
    ),
    nested = arrayOf<Any?>(
        arrayOf<Any?>(
            listOf<Record1>(),
            listOf<Record1>(
                Record1(
                    item = 2,
                ),
            ),
        ),
        arrayOf<Any?>(
            listOf<Record1>(
                Record1(
                    item = 3,
                ),
            ),
            listOf<Record1>(),
        ),
    ),
    reversed = arrayOf<Any?>(
        listOf<Record1>(
            Record1(
                item = 4,
            ),
        ),
        listOf<Record1>(),
    ),
)
