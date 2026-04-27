#+feature dynamic-literals
package main
ClientType_ :: struct { fetch: proc(..any) -> any }
AppType_ :: struct { client: ClientType_ }
app: AppType_

main :: proc() {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);
}
