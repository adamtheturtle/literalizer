data class Record0(val value: String)
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val item = Record0(
    value = "owned",
)
consume(value = item)
