import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue([JSONValue(true), JSONValue(false)]),
    JSONValue([JSONValue(true), JSONValue(true)]),
]);
}
