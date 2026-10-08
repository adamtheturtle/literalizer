fun f(value: Any? = null): Any? = null
val x = arrayOf(
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
        x,
    ),
))
