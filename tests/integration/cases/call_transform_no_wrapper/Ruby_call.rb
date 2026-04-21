class ApiType; def request(*a, **kw); end; end
class ClientType; def api; ApiType.new; end; end
client = ClientType.new
client.api.request(data: "hello")
client.api.request(data: 42)
client.api.request(data: true)
