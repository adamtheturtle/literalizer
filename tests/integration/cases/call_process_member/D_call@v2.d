import std.json;
void main() {
struct ProcessType_ { int fetch(T...)(T args) { return 0; } }
struct AppType_ { ProcessType_ process; }
AppType_ app;
app.process.fetch(JSONValue(["data": JSONValue("hello")]));
app.process.fetch(JSONValue(["data": JSONValue(42)]));
app.process.fetch(JSONValue(["data": JSONValue(true)]));
}
