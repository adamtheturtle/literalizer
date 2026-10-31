data class Record0(val name: String, val values: IntArray)
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val item = Record0(
    name = "first",
    values = intArrayOf(
        1,
        2,
    ),
)
consume(value = item)
