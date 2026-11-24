fun consume_widget(arg_value: Any? = null): Any? = listOf<Any?>(arg_value)
val ref_data = intArrayOf(
    1,
    2,
)
var my_data = intArrayOf(
    0,
)
consume_widget(arg_value = my_data)
my_data = ref_data
consume_widget(arg_value = my_data)
