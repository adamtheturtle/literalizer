import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue([JSONValue("name"), JSONValue("Alice")]),
    JSONValue([JSONValue("scores"), JSONValue(["1": JSONValue("first"), "2": JSONValue("second")])]),
]);
}
