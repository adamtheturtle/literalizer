struct Http_clientType; fetch; end
struct My_appType; http_client; end
my_app = My_appType(Http_clientType((args...; kwargs...) -> nothing))
my_app.http_client.fetch(payload="hello")
my_app.http_client.fetch(payload=42)
my_app.http_client.fetch(payload=true)
