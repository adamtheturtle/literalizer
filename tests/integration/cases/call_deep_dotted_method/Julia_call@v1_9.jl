struct ClientType; post; end
struct ApiType; client; end
struct ObjType; api; end
obj = ObjType(ApiType(ClientType((args...; kwargs...) -> nothing)))
obj.api.client.post(data="hello")
obj.api.client.post(data=42)
obj.api.client.post(data=true)
