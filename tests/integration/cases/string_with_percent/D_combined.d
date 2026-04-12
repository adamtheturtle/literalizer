import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue("100% done"),
    JSONValue("%(name) is here"),
]);
my_data = JSONValue([
    JSONValue("100% done"),
    JSONValue("%(name) is here"),
]);
}
