#+feature dynamic-literals
package main
_client_post_ :: proc(args: ..any) -> any { return nil }
ClientType_ :: struct { post: proc(..any) -> any }
ApiType_ :: struct { client: ClientType_ }
ObjType_ :: struct { api: ApiType_ }
obj: ObjType_ = ObjType_{ api = ApiType_{ client = ClientType_{ post = _client_post_ } } }

main :: proc() {
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(true);
}
