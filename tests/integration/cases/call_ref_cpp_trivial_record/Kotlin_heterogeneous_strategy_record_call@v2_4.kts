data class Record0(val value: Int)
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val item = Record0(
    value = 1,
)
consume(value = item)
