val my_data = mapOf<String, Any?>(
    "omap_value" to linkedMapOf<String, Any?>("first" to 1),
    "sibling_lists" to mapOf<String, Any?>("numbers" to listOf<Any?>(1, 2), "strings" to listOf<Any?>("x", "y")),
    "ref_marker_present" to arrayOf("\$keep", "z"),
)
