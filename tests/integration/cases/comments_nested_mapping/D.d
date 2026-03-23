import std.json;
void _check() {
    auto _v = JSONValue([
    "a": JSONValue(["x": JSONValue(1)]),
    "b": JSONValue(2),
]);
}
