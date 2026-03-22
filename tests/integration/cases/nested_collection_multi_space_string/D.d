import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue(["key": JSONValue("hello   world"), "value": JSONValue(1)]),
]);
}
