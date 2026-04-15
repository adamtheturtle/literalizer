struct ClientType; fetch; end
struct AppType; client; end
app = AppType(ClientType((args...; kwargs...) -> nothing))
app.client.fetch(payload="hello")
app.client.fetch(payload=42)
app.client.fetch(payload=true)
