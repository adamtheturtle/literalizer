fun make_widget(count: Any? = null): Any? = null
val my_data = make_widget(count = 42) ?
make_widget(count = 42) // inner
: nil // trailing
