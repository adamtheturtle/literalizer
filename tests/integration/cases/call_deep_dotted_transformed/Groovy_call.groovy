class _ClientType { def fetch(payload) { null } }
class _AppType { def client = new _ClientType() }
def app = new _AppType()
def emit(_arg) { null }
emit(app.client.fetch(payload: "hello"))
emit(app.client.fetch(payload: 42))
emit(app.client.fetch(payload: true))
