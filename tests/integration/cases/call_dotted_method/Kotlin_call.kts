class _ClientType { fun fetch(payload: Any? = null): Any? = null }
class _AppType { val client = _ClientType() }
val app = _AppType()
app.client.fetch(payload = "hello")
app.client.fetch(payload = 42)
app.client.fetch(payload = true)
