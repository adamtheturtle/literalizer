import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue([JSONValue(true), JSONValue(false)]),
    JSONValue([JSONValue(true), JSONValue(true)]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(true), JSONValue(false)]),
    JSONValue([JSONValue(true), JSONValue(true)]),
]);
}
