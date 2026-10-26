val my_data = mapOf<String, Any?>(
    "lists" to listOf<Any?>(intArrayOf(1), arrayOf("x"), arrayOf<Any?>()),
    "maps" to listOf<Map<String, Any?>>(mapOf<String, Any?>("x" to 1), mapOf<String, Any?>("x" to "s")),
    "empties" to mapOf<String, IntArray>("a" to intArrayOf(1), "b" to intArrayOf()),
)
