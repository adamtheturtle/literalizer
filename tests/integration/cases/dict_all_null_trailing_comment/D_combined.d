import std.json;
void _check() {
auto my_data = JSONValue([
    "a": JSONValue(null),
    "b": JSONValue(null),
    // trailing
]);
my_data = JSONValue([
    "a": JSONValue(null),
    "b": JSONValue(null),
    // trailing
]);
}
