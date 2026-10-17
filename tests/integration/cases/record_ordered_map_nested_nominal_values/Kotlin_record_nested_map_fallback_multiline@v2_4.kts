data class Record1(val x: Int)
data class Record0(val values: LinkedHashMap<String, Any?>, val flag: Boolean)
val my_data = Record0(
    values = linkedMapOf<String, Any?>(
        "outer" to linkedMapOf<String, Any?>(
            "inner" to Record1(
                x = 1,
            ),
        ),
    ),
    flag = true,
)
