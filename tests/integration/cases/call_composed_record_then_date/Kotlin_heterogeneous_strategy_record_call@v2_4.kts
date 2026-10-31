import java.time.LocalDate
data class Record0(val a: Int)
fun consume(stamp: Any? = null, value: Any? = null): Any? = listOf<Any?>(stamp, value)
val item = Record0(
    a = 1,
)
val stamp = LocalDate.of(2001, 2, 3)
consume(stamp = stamp, value = item)
