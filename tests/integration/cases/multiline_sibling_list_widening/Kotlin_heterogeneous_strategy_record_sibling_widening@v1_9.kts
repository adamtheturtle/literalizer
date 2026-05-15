data class Record1(val numbers: IntArray, val strings: Array<String>)
data class Record0(val omap_value: LinkedHashMap<String, Any?>, val sibling_lists: Record1, val ref_marker_present: Array<String>)
val my_data = Record0(
    omap_value = linkedMapOf<String, Any?>(
        "first" to 1,
    ),
    sibling_lists = Record1(
        numbers = intArrayOf(
            1,
            2,
        ),
        strings = arrayOf(
            "x",
            "y",
        ),
    ),
    ref_marker_present = arrayOf(
        "\$keep",
        "z",
    ),
)
