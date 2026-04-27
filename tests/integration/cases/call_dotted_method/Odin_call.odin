#+feature dynamic-literals
package main
_client_fetch_ :: proc(args: ..any) -> any { return nil }
ClientType_ :: struct { fetch: proc(..any) -> any }
AppType_ :: struct { client: ClientType_ }
app: AppType_ = AppType_{ client = ClientType_{ fetch = _client_fetch_ } }

main :: proc() {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);
}
