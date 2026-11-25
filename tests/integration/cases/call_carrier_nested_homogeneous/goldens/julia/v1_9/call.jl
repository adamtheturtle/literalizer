struct ClientType; go; end
struct AppType; client; end
app = AppType(ClientType((args...; kwargs...) -> nothing))
app.client.go(first_value=[1], second_value=[2])
