import std.json;

void _check() {
    auto _v = JSONValue([
    JSONValue([JSONValue([JSONValue(1), JSONValue(2)]), JSONValue([JSONValue(3), JSONValue(4)])]),
    JSONValue([JSONValue([JSONValue(5)])]),
]);
}
