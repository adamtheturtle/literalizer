fun make_widget(value: Any? = null): Any? = listOf<Any?>(value)
fun consume(value: Any? = null): Any? = listOf<Any?>(value)
val my_data = make_widget(value = 42)
consume(value = my_data)
