import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue("a"),
    //
    JSONValue("b"),
]);
my_data = JSONValue([
    JSONValue("a"),
    //
    JSONValue("b"),
]);
}
