data class Record0(val values: LinkedHashMap<String, Any?>, val flag: Boolean, val nested_values: LinkedHashMap<String, Any?>, val list_values: LinkedHashMap<String, Any?>)
val my_data = Record0(
    values = linkedMapOf<String, Any?>(
        "first" to 2208988800L,
    ),
    flag = true,
    nested_values = linkedMapOf<String, Any?>(
        "first" to linkedMapOf<String, Any?>(
            "nested" to 2208988800L,
        ),
    ),
    list_values = linkedMapOf<String, Any?>(
        "first" to arrayOf(
            2208988800L,
        ),
    ),
)
