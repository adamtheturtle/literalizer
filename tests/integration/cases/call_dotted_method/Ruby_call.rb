class ClientType; def fetch(*a, **kw); end; end
class AppType; def client; ClientType.new; end; end
app = AppType.new
app.client.fetch(payload: "hello")
app.client.fetch(payload: 42)
app.client.fetch(payload: true)
