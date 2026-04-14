object Check {
class _ClientType { def fetch(payload: Any = null): Any = null }
class _AppType { val client = new _ClientType }
val app = new _AppType
def emit(_arg: Any = null): Any = null
emit(app.client.fetch(payload = "hello"))
emit(app.client.fetch(payload = 42))
emit(app.client.fetch(payload = true))
}
