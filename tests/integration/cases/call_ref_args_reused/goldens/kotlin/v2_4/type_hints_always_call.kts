fun process(data: Any? = null, count: Any? = null): Any? = listOf<Any?>(data, count)
val single_var: IntArray = intArrayOf(
    4,
    5,
    6,
)
val repeated_var: Int = 1
process(data = repeated_var, count = 1)
process(data = single_var, count = 0)
process(data = repeated_var, count = 8)
