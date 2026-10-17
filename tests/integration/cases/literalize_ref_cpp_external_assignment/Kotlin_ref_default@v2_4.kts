fun consume_widget(_arg: Any? = null): Any? = listOf<Any?>(_arg)
val ref_data = intArrayOf(
    1,
    2,
)
val my_data = intArrayOf(
    0,
)
consume_widget(_arg = my_data)
my_data = ref_data
consume_widget(_arg = my_data)
