fun make_widget(count: Any? = null): Any? = listOf<Any?>(count)
var my_data = make_widget(count = null)
my_data = make_widget(count = 42) // note
