data class Record1(val pair: List<Any?>)
data class Record0(val outer: Record1)
val my_data: List<Record0> = listOf<Record0>(
    Record0(outer = Record1(pair = listOf<Any?>(1, "first"))),
    Record0(outer = Record1(pair = listOf<Any?>(false, "second"))),
)
