class ClientType; def post(*a, **kw); end; end
class ApiType; def client; ClientType.new; end; end
class ObjType; def api; ApiType.new; end; end
obj = ObjType.new
obj.api.client.post(data: "hello")
obj.api.client.post(data: 42)
obj.api.client.post(data: true)
