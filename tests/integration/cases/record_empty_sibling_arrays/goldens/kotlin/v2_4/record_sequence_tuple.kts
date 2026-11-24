data class Record1(val item: Int)
data class Record2(val item: Any?)
data class Record0(val integers: Pair<List<Any?>, List<Record1>>, val nulls: Pair<List<Any?>, List<Record2>>, val nested: Pair<Pair<List<Any?>, List<Record1>>, Pair<List<Record1>, List<Any?>>>, val reversed: Pair<List<Record1>, List<Any?>>)
val my_data = Record0(
    integers = Pair(
        listOf<Record1>(),
        listOf<Record1>(
            Record1(
                item = 1,
            ),
        ),
    ),
    nulls = Pair(
        listOf<Record2>(),
        listOf<Record2>(
            Record2(
                item = null,
            ),
        ),
    ),
    nested = Pair(
        Pair(
            listOf<Record1>(),
            listOf<Record1>(
                Record1(
                    item = 2,
                ),
            ),
        ),
        Pair(
            listOf<Record1>(
                Record1(
                    item = 3,
                ),
            ),
            listOf<Record1>(),
        ),
    ),
    reversed = Pair(
        listOf<Record1>(
            Record1(
                item = 4,
            ),
        ),
        listOf<Record1>(),
    ),
)
