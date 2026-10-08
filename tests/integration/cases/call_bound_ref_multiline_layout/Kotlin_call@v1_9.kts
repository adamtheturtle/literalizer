fun f(value: Any? = null): Any? = null
val ref_data = arrayOf(
    intArrayOf(
        1,
        2,
    ),
    intArrayOf(
        3,
        4,
    ),
)
f(value = arrayOf(
    arrayOf(
        ref_data,
    ),
))
