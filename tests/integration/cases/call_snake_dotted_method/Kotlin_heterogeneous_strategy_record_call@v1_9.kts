class _Http_ClientType { fun fetch(@Suppress("UNUSED_PARAMETER") payload: Any? = null): Any? = null }
class _My_AppType { val http_client = _Http_ClientType() }
val my_app = _My_AppType()
my_app.http_client.fetch(payload = "hello")
my_app.http_client.fetch(payload = 42)
my_app.http_client.fetch(payload = true)
