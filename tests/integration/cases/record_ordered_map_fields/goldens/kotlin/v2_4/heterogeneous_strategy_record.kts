data class Record0(val numbers: LinkedHashMap<String, Any?>, val words: LinkedHashMap<String, Any?>, val nested: LinkedHashMap<String, Any?>, val empty: LinkedHashMap<String, Any?>, val flag: Boolean, val nested_maps: LinkedHashMap<String, Any?>, val empty_nested_maps: LinkedHashMap<String, Any?>)
val my_data = Record0(
    numbers = linkedMapOf<String, Any?>(
        "first" to 1,
    ),
    words = linkedMapOf<String, Any?>(
        "first" to "s",
    ),
    nested = linkedMapOf<String, Any?>(
        "first" to intArrayOf(
            1,
            2,
        ),
    ),
    empty = linkedMapOf<String, Any?>(),
    flag = true,
    nested_maps = linkedMapOf<String, Any?>(
        "first" to linkedMapOf<String, Any?>(
            "nested" to 1,
        ),
    ),
    empty_nested_maps = linkedMapOf<String, Any?>(
        "first" to linkedMapOf<String, Any?>(),
    ),
)
