fun process(data: Any? = null, count: Any? = null): Any? = null
val my_ints = intArrayOf(
    1,
    2,
    3,
)
val my_strings = arrayOf(
    "a",
    "b",
)
val my_empty = listOf<Any?>()
process(data = my_ints, count = 42)
process(data = my_strings, count = 7)
process(data = my_empty, count = 99)
