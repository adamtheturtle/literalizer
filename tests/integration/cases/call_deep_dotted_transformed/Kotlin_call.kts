class _ClientType { fun fetch(payload: Any? = null): Any? = null }
class _AppType { val client = _ClientType() }
val app = _AppType()
fun emit(_arg: Any? = null): Any? = null
emit(app.client.fetch(payload = "hello"))
emit(app.client.fetch(payload = 42))
emit(app.client.fetch(payload = true))
