data class Record0(val id: Int)
var shared = listOf<Record0>(
    Record0(id = 1),
)
var second = listOf<Record0>(
    Record0(id = 2),
)
var my_data = listOf<Any?>(
    shared,
    second,
)
my_data = listOf<Any?>(
    shared,
    second,
)
