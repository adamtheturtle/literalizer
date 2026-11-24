fun consume_widget(arg_value: Any? = null): Any? = listOf<Any?>(arg_value)
val shared = intArrayOf(
    1,
    2,
)
val my_data = shared
consume_widget(arg_value = my_data)
