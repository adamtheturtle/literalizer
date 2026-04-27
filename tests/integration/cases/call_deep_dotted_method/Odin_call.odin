#+feature dynamic-literals
package main
ClientType_ :: struct { post: proc(..any) -> any }
ApiType_ :: struct { client: ClientType_ }
ObjType_ :: struct { api: ApiType_ }
obj: ObjType_

main :: proc() {
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(true);
}
