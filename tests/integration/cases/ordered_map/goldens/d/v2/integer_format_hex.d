import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("name"), JSONValue("Alice")]),
    JSONValue([JSONValue("age"), JSONValue(0x1e)]),
    JSONValue([JSONValue("active"), JSONValue(true)]),
]);
}
