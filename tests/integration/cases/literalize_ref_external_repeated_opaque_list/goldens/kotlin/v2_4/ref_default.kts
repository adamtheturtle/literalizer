fun consume_widget(arg_value: Any? = null): Any? = listOf<Any?>(arg_value)
val item = arrayOf<Any?>()
val my_data = arrayOf<Any?>(
    item,
    item,
)
consume_widget(arg_value = my_data)
