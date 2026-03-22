import std.json;

void _check() {
auto my_data = JSONValue([
    JSONValue(true),
    JSONValue("hi"),
    JSONValue([JSONValue(1), JSONValue(2)]),
    JSONValue(null),
]);
}
