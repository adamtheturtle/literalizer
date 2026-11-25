struct ClientType; fetch; end
struct AppType; client; end
app = AppType(ClientType((args...; kwargs...) -> nothing))
emit(args...; kwargs...) = nothing
emit(app.client.fetch(payload="hello"))
emit(app.client.fetch(payload=42))
emit(app.client.fetch(payload=true))
