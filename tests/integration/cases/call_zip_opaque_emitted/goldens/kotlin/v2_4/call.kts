import java.time.LocalDateTime
fun process(value: Any? = null): Any? = listOf<Any?>(value)
fun emit(_call: Any? = null, _zip: Any? = null): Any? = listOf<Any?>(_call, _zip)
emit(process(value = 1), LocalDateTime.of(2024, 1, 15, 12, 0, 0))
