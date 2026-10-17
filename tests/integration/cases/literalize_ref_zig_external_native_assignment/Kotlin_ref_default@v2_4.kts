fun consume_widget(_arg: Any? = null): Any? = listOf<Any?>(_arg)
val shared = intArrayOf(
    1,
    2,
)
var my_data = intArrayOf(
    0,
)
consume_widget(_arg = my_data)
my_data = shared
consume_widget(_arg = my_data)
