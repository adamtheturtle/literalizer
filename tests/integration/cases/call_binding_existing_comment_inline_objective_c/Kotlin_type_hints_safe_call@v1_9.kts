fun make_widget(count: Any? = null): Any? = listOf<Any?>(count)
var my_data = make_widget(count = 42)
my_data = make_widget(count = my_data) // note
make_widget(count = my_data)
