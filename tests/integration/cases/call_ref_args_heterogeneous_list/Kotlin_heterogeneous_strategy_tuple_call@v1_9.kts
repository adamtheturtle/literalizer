fun process(@Suppress("UNUSED_PARAMETER") data: Any? = null, @Suppress("UNUSED_PARAMETER") count: Any? = null): Any? = null
val my_ints = intArrayOf(
    1,
    2,
    3,
)
val my_strings = arrayOf(
    "a",
    "b",
)
val my_empty = arrayOf<Any?>()
process(data = my_ints, count = 42)
process(data = my_strings, count = 7)
process(data = my_empty, count = 99)
