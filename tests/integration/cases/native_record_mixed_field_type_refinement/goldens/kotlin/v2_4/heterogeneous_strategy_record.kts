data class Record2(val value: Int)
data class Record1(val items: List<Any?>)
data class Record3(val value: String)
data class Record0(val first: Record1, val second: Record1)
val my_data = Record0(
    first = Record1(
        items = listOf<Any?>(
            1,
            Record2(
                value = 2,
            ),
        ),
    ),
    second = Record1(
        items = listOf<Any?>(
            1,
            Record3(
                value = "s",
            ),
        ),
    ),
)
