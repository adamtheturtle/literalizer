import std.json;
void _check() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue(1)]),
    "b": JSONValue([JSONValue("x")]),
]);
}
