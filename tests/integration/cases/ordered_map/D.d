import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue([JSONValue("name"), JSONValue("Alice")]),
    JSONValue([JSONValue("age"), JSONValue(30)]),
    JSONValue([JSONValue("active"), JSONValue(true)]),
]);
}
