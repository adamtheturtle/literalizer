import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue([JSONValue(1), JSONValue(2)]),
    JSONValue([JSONValue("a"), JSONValue("b")]),
]);
}
