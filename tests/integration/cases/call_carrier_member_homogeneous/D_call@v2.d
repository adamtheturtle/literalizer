import std.json;
void main() {
struct AppType_ { int go(T...)(T args) { return 0; } }
AppType_ app;
app.go(JSONValue([JSONValue(1)]), JSONValue([JSONValue(2)]));
}
