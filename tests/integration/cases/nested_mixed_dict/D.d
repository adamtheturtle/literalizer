import std.json;
void _check() {
auto my_data = JSONValue([
    "outer": JSONValue(["a": JSONValue(1), "b": JSONValue("x"), "c": JSONValue(null)]),
]);
}
