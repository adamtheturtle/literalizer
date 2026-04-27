#+feature dynamic-literals
package main
ClientType_ :: struct { fetch: proc(..any) -> any }
AppType_ :: struct { client: ClientType_ }
app: AppType_
emit :: proc(args: ..any) -> any { return nil }

main :: proc() {
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(true));
}
