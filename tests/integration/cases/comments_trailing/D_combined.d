import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue("a"),
    // trailing
]);
my_data = JSONValue([
    JSONValue("a"),
    // trailing
]);
}
