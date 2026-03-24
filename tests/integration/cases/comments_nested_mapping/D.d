import std.json;
void _check() {
auto my_data = JSONValue([
    "a": JSONValue(["x": JSONValue(1)]),
    "b": JSONValue(2),
]);
}
