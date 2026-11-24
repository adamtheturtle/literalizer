class ClientType; def fetch(*a, **kw); end; end
class AppType; def client; ClientType.new; end; end
app = AppType.new
app.client.fetch(value: "hello")
app.client.fetch(value: "world")
