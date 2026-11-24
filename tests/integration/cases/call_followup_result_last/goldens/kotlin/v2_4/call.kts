fun make_widget(first: Any? = null, second: Any? = null): Any? = listOf<Any?>(first, second)
fun consume(first: Any? = null, second: Any? = null): Any? = listOf<Any?>(first, second)
val my_data = make_widget(first = 42, second = 3)
consume(first = 3, second = my_data)
