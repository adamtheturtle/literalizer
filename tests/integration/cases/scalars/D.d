import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue(42),
    JSONValue(3.14),
    JSONValue(true),
    JSONValue(false),
    JSONValue("hello \"world\""),
]);
}
