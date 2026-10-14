fun make_widget(count: Any? = null): Any? = listOf<Any?>(count)
val my_data = ("\"prefix ${"// payload"}\"").length >= 0 ? make_widget(count = 42) : make_widget(count = 42)
