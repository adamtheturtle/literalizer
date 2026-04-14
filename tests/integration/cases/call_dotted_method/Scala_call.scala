object Check {
class _ClientType { def send(payload: Any = null): Any = null }
class _NsType { val client = new _ClientType }
val ns = new _NsType
ns.client.send(payload = "hello")
ns.client.send(payload = 42)
ns.client.send(payload = true)
}
