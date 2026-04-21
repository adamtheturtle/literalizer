class _ApiType { fun request(data: Any? = null): Any? = null }
class _ClientType { val api = _ApiType() }
val client = _ClientType()
client.api.request(data = "hello")
client.api.request(data = 42)
client.api.request(data = true)
