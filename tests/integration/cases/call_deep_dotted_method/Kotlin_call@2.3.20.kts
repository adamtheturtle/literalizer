class _ClientType { fun post(data: Any? = null): Any? = null }
class _ApiType { val client = _ClientType() }
class _ObjType { val api = _ApiType() }
val obj = _ObjType()
obj.api.client.post(data = "hello")
obj.api.client.post(data = 42)
obj.api.client.post(data = true)
