#+feature dynamic-literals
package main
_client_go_ :: proc(args: ..any) -> any { return nil }
ClientType_ :: struct { go: proc(..any) -> any }
AppType_ :: struct { client: ClientType_ }

main :: proc() {
app: AppType_ = AppType_{ client = ClientType_{ go = _client_go_ } }
app.client.go([dynamic]any{1}, [dynamic]any{2});
}
