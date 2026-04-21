struct ApiType; request; end
struct ClientType; api; end
client = ClientType(ApiType((args...; kwargs...) -> nothing))
client.api.request(data="hello")
client.api.request(data=42)
client.api.request(data=true)
