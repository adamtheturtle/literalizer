val my_data = mapOf<String, Any?>(
    "positive" to arrayOf<Any?>(mapOf<String, Any?>("item" to arrayOf<Any?>(2147483648L))),
    "negative" to arrayOf<Any?>(mapOf<String, Any?>("item" to arrayOf<Any?>(-2147483649L))),
    "mixed" to arrayOf<Any?>(mapOf<String, Any?>("item" to arrayOf<Any?>(0L, 2147483648L))),
)
