data class Record2(val x: Int)
data class Record1(val values: LinkedHashMap<String, Any?>, val flag: Boolean)
data class Record3(val y: Int)
data class Record0(val first: Record1, val second: Record1)
val my_data = Record0(
    first = Record1(
        values = linkedMapOf<String, Any?>(
            "item" to Record2(
                x = 1,
            ),
        ),
        flag = true,
    ),
    second = Record1(
        values = linkedMapOf<String, Any?>(
            "item" to Record3(
                y = 2,
            ),
        ),
        flag = false,
    ),
)
