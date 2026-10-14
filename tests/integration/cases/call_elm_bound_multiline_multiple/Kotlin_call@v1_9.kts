fun f(value: Any? = null): Any? = listOf<Any?>(value)
val ref_data = intArrayOf(
    1,
    2,
)
f(value = arrayOf(
    ref_data,
))
f(value = arrayOf(
    ref_data,
))
