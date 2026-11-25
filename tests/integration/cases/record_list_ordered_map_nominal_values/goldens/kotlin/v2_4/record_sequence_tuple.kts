data class Record1(val x: Int)
data class Record0(val values: Pair<LinkedHashMap<String, Any?>, LinkedHashMap<String, Any?>>, val flag: Boolean)
val my_data = Record0(
    values = Pair(
        linkedMapOf<String, Any?>(
            "inner" to Record1(
                x = 1,
            ),
        ),
        linkedMapOf<String, Any?>(
            "inner" to Record1(
                x = 2,
            ),
        ),
    ),
    flag = true,
)
