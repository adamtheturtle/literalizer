fun consume_widget(_arg: Any? = null): Any? = listOf<Any?>(_arg)
val item = intArrayOf(
    1,
    2,
)
val my_data = intArrayOf(
    1,
    2,
)
consume_widget(_arg = my_data)
my_data = item
consume_widget(_arg = my_data)
