import std.json;

void _check() {
    auto _v = JSONValue([
    JSONValue([JSONValue(1), JSONValue("a")]),
    JSONValue([JSONValue(2), JSONValue("b")]),
]);
}
