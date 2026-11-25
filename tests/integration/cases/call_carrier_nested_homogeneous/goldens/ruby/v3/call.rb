class ClientType; def go(*a, **kw); end; end
class AppType; def client; ClientType.new; end; end
app = AppType.new
app.client.go(first_value: [1], second_value: [2])
