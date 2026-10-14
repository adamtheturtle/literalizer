fun make_widget(count: Any? = null): Any? = listOf<Any?>(count)
val my_data = make_widget(count = 42) ?
make_widget(count = 42) // inner
: nil // trailing
