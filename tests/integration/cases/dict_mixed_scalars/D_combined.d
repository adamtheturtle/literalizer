import std.json;
void _check() {
auto my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue("x"),
]);
my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue("x"),
]);
}
