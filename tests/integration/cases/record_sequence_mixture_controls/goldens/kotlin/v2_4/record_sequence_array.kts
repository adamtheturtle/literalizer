data class Record0(val x: Int)
val my_data = arrayOf<Any?>(
    listOf<Any?>(arrayOf<Any?>(1), Record0(x = 1)),
    listOf<Record0>(Record0(x = 1), Record0(x = 2)),
    arrayOf<Any?>(listOf<Record0>(), listOf<Record0>(Record0(x = 1))),
    arrayOf<Any?>(arrayOf<Any?>(), arrayOf<Any?>()),
)
