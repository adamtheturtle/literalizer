fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val item: IntArray = intArrayOf(
    1,
    2,
)
consume(value = item)
