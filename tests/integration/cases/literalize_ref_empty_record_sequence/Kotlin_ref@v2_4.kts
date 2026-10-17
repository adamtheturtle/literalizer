data class Record0(val x: Int)
val emptyItems = listOf<Record0>()
val populatedItems = listOf<Record0>(
    Record0(x = 1),
)
val my_data = listOf<Any?>(
    emptyItems,
    populatedItems,
)
