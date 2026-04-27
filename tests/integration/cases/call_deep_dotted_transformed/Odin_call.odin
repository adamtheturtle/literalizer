#+feature dynamic-literals
package main
_client_fetch_ :: proc(args: ..any) -> any { return nil }
ClientType_ :: struct { fetch: proc(..any) -> any }
AppType_ :: struct { client: ClientType_ }
app: AppType_ = AppType_{ client = ClientType_{ fetch = _client_fetch_ } }
emit :: proc(args: ..any) -> any { return nil }

main :: proc() {
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(true));
}
