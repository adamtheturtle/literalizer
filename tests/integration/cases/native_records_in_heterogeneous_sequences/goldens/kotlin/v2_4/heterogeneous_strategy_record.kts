data class Record1(val k: BooleanArray)
data class Record0(val h: List<Any?>)
val my_data = Record0(
    h = listOf<Any?>(
        1,
        "a",
        listOf<Any?>(
            2,
            "b",
        ),
        Record1(
            k = booleanArrayOf(
                true,
            ),
        ),
    ),
)
