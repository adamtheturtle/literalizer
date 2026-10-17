fun make_widget(count: Any? = null): Any? = listOf<Any?>(count)
var my_data = make_widget(count = 42)
make_widget(count = my_data)
my_data = make_widget(count = my_data) // note
// extra
make_widget(count = my_data)
