class _ClientType { def fetch(Map _args) { null } }
class _AppType { def client = new _ClientType() }
def app = new _AppType()
app.client.fetch(value: "hello")
app.client.fetch(value: "world")
