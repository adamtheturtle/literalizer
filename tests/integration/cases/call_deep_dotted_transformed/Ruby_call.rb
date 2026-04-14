class ClientType; def fetch(*a, **kw); end; end
class AppType; def client; ClientType.new; end; end
app = AppType.new
def emit(*a); end
emit(app.client.fetch(payload: "hello"))
emit(app.client.fetch(payload: 42))
emit(app.client.fetch(payload: true))
