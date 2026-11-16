import std.json;
void main() {
int consume(T...)(T args) { return 0; }
auto item = JSONValue(42);
consume(JSONValue(["field": item]));
}
