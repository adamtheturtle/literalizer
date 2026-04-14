class _ClientType { fun send(payload: Any? = null): Any? = null }
class _NsType { val client = _ClientType() }
val ns = _NsType()
ns.client.send(payload = "hello")
ns.client.send(payload = 42)
ns.client.send(payload = true)
