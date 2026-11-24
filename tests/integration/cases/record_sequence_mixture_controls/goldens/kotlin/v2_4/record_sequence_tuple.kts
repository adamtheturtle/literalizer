data class Record0(val x: Int)
val my_data = listOf<Any?>(
    listOf<Any?>(listOf<Any?>(1), Record0(x = 1)),
    listOf<Record0>(Record0(x = 1), Record0(x = 2)),
    Pair(listOf<Record0>(), listOf<Record0>(Record0(x = 1))),
    Pair(listOf<Any?>(), listOf<Any?>()),
)
