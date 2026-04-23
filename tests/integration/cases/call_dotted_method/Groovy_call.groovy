class _ClientType { def fetch(Map _args) { null } }
class _AppType { def client = new _ClientType() }
def app = new _AppType()
app.client.fetch(payload: "hello")
app.client.fetch(payload: 42)
app.client.fetch(payload: true)
