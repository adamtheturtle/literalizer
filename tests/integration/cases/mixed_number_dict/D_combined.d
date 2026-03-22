import std.json;
void _check() {
auto my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue(2.5),
    "c": JSONValue(3),
]);
my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue(2.5),
    "c": JSONValue(3),
]);
}
