import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue([JSONValue(1.5), JSONValue(2.5)]),
    JSONValue([JSONValue(3.5), JSONValue(4.5)]),
]);
}
