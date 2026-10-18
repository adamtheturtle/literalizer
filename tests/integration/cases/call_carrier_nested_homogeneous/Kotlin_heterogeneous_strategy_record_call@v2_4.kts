class _ClientType { fun go(first_value: Any? = null, second_value: Any? = null): Any? = listOf<Any?>(first_value, second_value) }
class _AppType { val client = _ClientType() }
val app = _AppType()
app.client.go(first_value = intArrayOf(1), second_value = intArrayOf(2))
