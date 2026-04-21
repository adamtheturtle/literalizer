object Check {
class _ApiType { def request(data: Any = null): Any = null }
class _ClientType { val api = new _ApiType }
val client = new _ClientType
client.api.request(data = "hello")
client.api.request(data = 42)
client.api.request(data = true)
}
