data class Record1(val x: Int)
data class Record0(val values: LinkedHashMap<String, Any?>, val flag: Boolean)
val my_data = Record0(
    values = linkedMapOf<String, Any?>(
        "first" to Record1(
            x = 1,
        ),
        "second" to Record1(
            x = 2,
        ),
    ),
    flag = true,
)
