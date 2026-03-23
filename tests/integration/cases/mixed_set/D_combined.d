import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue(true),
    JSONValue(42),
    JSONValue("apple"),
]);
my_data = JSONValue([
    JSONValue(true),
    JSONValue(42),
    JSONValue("apple"),
]);
}
