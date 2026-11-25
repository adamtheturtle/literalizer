class _ClientType { def fetch(Map _args) { null } }
class _AppType { def client = new _ClientType() }
def app = new _AppType()
def emit(Map _args) { null }
emit(app.client.fetch(payload: "hello"))
emit(app.client.fetch(payload: 42))
emit(app.client.fetch(payload: true))
