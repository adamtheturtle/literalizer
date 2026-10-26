import std.json;
void main() {
struct ApiType_ { int process(T...)(T args) { return 0; } }
ApiType_ api;
api.process(parseJSON("{}"));
}
