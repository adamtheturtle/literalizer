import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue(true),
    JSONValue(false),
    JSONValue(true),
]);
my_data = JSONValue([
    JSONValue(true),
    JSONValue(false),
    JSONValue(true),
]);
}
