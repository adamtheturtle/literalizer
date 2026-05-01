import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("a"), parseJSON("[]")]),
    JSONValue([JSONValue("b"), JSONValue(1)]),
]);
}
