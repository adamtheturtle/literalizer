import std.json;
void _check() {
auto my_data = JSONValue([
    "name": JSONValue("Alice"),
    "tags": JSONValue([JSONValue(true), JSONValue(42), JSONValue("apple")]),
]);
}
