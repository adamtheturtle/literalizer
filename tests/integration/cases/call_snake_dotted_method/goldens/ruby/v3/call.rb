class HttpClientType; def fetch(*a, **kw); end; end
class MyAppType; def http_client; HttpClientType.new; end; end
my_app = MyAppType.new
my_app.http_client.fetch(payload: "hello")
my_app.http_client.fetch(payload: 42)
my_app.http_client.fetch(payload: true)
