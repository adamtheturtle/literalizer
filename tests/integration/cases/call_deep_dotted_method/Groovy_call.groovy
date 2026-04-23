class _ClientType { def post(Map _args) { null } }
class _ApiType { def client = new _ClientType() }
class _ObjType { def api = new _ApiType() }
def obj = new _ObjType()
obj.api.client.post(data: "hello")
obj.api.client.post(data: 42)
obj.api.client.post(data: true)
