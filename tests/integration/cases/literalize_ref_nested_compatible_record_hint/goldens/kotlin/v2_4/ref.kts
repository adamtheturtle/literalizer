data class Record1(val items: IntArray)
data class Record0(val outer: Record1)
val recordData = Record1(
    items = intArrayOf(
        1,
        2,
    ),
)
val my_data = Record0(
    outer = recordData,
)
