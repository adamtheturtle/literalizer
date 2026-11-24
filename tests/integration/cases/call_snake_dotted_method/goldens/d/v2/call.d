import std.json;
void main() {
struct Http_ClientType_ { int fetch(T...)(T args) { return 0; } }
struct My_AppType_ { Http_ClientType_ http_client; }
My_AppType_ my_app;
my_app.http_client.fetch("hello");
my_app.http_client.fetch(42);
my_app.http_client.fetch(true);
}
