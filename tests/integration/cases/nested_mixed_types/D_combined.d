import std.json;

void _check() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue(2)]),
    JSONValue([JSONValue("a"), JSONValue("b")]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue(2)]),
    JSONValue([JSONValue("a"), JSONValue("b")]),
]);
}
