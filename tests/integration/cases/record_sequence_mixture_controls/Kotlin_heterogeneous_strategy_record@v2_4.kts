data class Record0(val x: Int)
val my_data = listOf<Any?>(
    listOf<Any?>(intArrayOf(1), Record0(x = 1)),
    listOf<Record0>(Record0(x = 1), Record0(x = 2)),
    listOf<Any?>(listOf<Record0>(), listOf<Record0>(Record0(x = 1))),
    listOf<Any?>(arrayOf<Any?>(), arrayOf<Any?>()),
)
