#+feature dynamic-literals
package main
_http_client_fetch_ :: proc(args: ..any) -> any { return nil }
Http_ClientType_ :: struct { fetch: proc(..any) -> any }
My_AppType_ :: struct { http_client: Http_ClientType_ }
my_app: My_AppType_ = My_AppType_{ http_client = Http_ClientType_{ fetch = _http_client_fetch_ } }

main :: proc() {
my_app.http_client.fetch("hello");
my_app.http_client.fetch(42);
my_app.http_client.fetch(true);
}
