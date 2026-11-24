fun consume_widget(arg_value: Any? = null): Any? = listOf<Any?>(arg_value)
val shared = 1
val my_data = shared
consume_widget(arg_value = my_data)
