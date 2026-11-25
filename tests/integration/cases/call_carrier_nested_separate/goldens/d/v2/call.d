import std.json;
void main() {
struct ClientType_ { int go(T...)(T args) { return 0; } }
struct AppType_ { ClientType_ client; }
AppType_ app;
app.client.go(JSONValue([JSONValue(1)]), JSONValue([JSONValue("text")]));
}
