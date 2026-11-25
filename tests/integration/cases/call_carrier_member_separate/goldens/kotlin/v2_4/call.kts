class _AppType { fun go(first_value: Any? = null, second_value: Any? = null): Any? = listOf<Any?>(first_value, second_value) }
val app = _AppType()
app.go(first_value = intArrayOf(1), second_value = arrayOf("text"))
