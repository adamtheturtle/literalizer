data class Record1(val item: Int)
data class Record2(val item: Any?)
data class Record0(val integers: List<Any?>, val nulls: List<Any?>, val nested: List<Any?>, val reversed: List<Any?>)
val my_data = Record0(
    integers = listOf<Any?>(
        listOf<Record1>(),
        listOf<Record1>(
            Record1(
                item = 1,
            ),
        ),
    ),
    nulls = listOf<Any?>(
        listOf<Record2>(),
        listOf<Record2>(
            Record2(
                item = null,
            ),
        ),
    ),
    nested = listOf<Any?>(
        listOf<Any?>(
            listOf<Record1>(),
            listOf<Record1>(
                Record1(
                    item = 2,
                ),
            ),
        ),
        listOf<Any?>(
            listOf<Record1>(
                Record1(
                    item = 3,
                ),
            ),
            listOf<Record1>(),
        ),
    ),
    reversed = listOf<Any?>(
        listOf<Record1>(
            Record1(
                item = 4,
            ),
        ),
        listOf<Record1>(),
    ),
)
