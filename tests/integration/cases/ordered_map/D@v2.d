import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("name"), JSONValue("Alice")]),
    JSONValue([JSONValue("age"), JSONValue(30)]),
    JSONValue([JSONValue("active"), JSONValue(true)]),
]);
}
