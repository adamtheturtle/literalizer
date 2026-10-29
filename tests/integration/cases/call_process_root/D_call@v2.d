import std.json;
void main() {
struct ApiType_ { int fetch(T...)(T args) { return 0; } }
struct ProcessType_ { ApiType_ api; }
ProcessType_ process;
process.api.fetch(JSONValue(["data": JSONValue("hello")]));
process.api.fetch(JSONValue(["data": JSONValue(42)]));
process.api.fetch(JSONValue(["data": JSONValue(true)]));
}
