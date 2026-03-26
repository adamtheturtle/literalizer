import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["name": JSONValue("Alice")]), JSONValue(["name": JSONValue("Bob")])]),
    JSONValue([JSONValue(["name": JSONValue("Charlie")]), JSONValue(["name": JSONValue("Dave")])]),
]);
}
