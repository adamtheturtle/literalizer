import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["name": JSONValue("Alice")]), JSONValue(["name": JSONValue("Bob")])]),
    JSONValue([JSONValue(["name": JSONValue("Charlie")]), JSONValue(["name": JSONValue("Dave")])]),
]);
}
