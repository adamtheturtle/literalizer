class _ClientType { fun fetch(@Suppress("UNUSED_PARAMETER") value: Any? = null): Any? = null }
class _AppType { val client = _ClientType() }
val app = _AppType()
app.client.fetch(value = "hello")
app.client.fetch(value = "world")
