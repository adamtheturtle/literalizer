import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue(42),
    JSONValue(3.14),
    JSONValue(true),
    JSONValue(false),
    JSONValue("hello \"world\""),
]);
}
