data class Record1(val pair: Array<Any?>)
data class Record0(val outer: Record1)
val my_data = listOf<Record0>(
    Record0(outer = Record1(pair = arrayOf<Any?>(1, "first"))),
    Record0(outer = Record1(pair = arrayOf<Any?>(false, "second"))),
)
