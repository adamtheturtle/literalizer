import std.json;
void main() {
struct ClientType_ { int fetch(T...)(T args) { return 0; } }
struct AppType_ { ClientType_ client; }
AppType_ app;
app.client.fetch("hello");
app.client.fetch("world");
}
