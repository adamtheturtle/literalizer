import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue(true),
    JSONValue("hi"),
    JSONValue([JSONValue(1), JSONValue(2)]),
    JSONValue(null),
]);
}
