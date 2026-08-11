fun consume(items: Any? = null, mapping: Any? = null): Any? = null
val foo = 42
consume(items = listOf<Map<String, Int>>(
    mapOf<String, Any?>(
        "other" to 1,
    ),
    foo,
), mapping = mapOf<String, Int>(
    "left" to foo,
    "other" to 1,
))
