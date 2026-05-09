struct ClientType; fetch; end
struct AppType; client; end
app = AppType(ClientType((args...; kwargs...) -> nothing))
app.client.fetch(value="hello")
app.client.fetch(value="world")
