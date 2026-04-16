import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue([JSONValue([JSONValue("a"), JSONValue(1)])]),
    JSONValue("hello"),
]);
my_data = JSONValue([
    JSONValue([JSONValue([JSONValue("a"), JSONValue(1)])]),
    JSONValue("hello"),
]);
}
