fun consume_widget(arg_value: Any? = null): Any? = listOf<Any?>(arg_value)
var my_data = 0
val shared = 1
my_data = shared
consume_widget(arg_value = my_data)
