fun make_widget(count: Any? = null): Any? = listOf<Any?>(count)
fun consume_widget(count: Any? = null): Any? = listOf<Any?>(count)
var my_data = make_widget(count = 42)
consume_widget(count = my_data)
my_data = make_widget(count = 42) // note
// extra
consume_widget(count = my_data)
