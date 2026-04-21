class _ApiType { def request(data) { null } }
class _ClientType { def api = new _ApiType() }
def client = new _ClientType()
client.api.request(data: "hello")
client.api.request(data: 42)
client.api.request(data: true)
