import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue("a")]),
    JSONValue([JSONValue(2), JSONValue("b")]),
]);
}
