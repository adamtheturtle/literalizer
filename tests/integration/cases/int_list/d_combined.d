import std.json;

void _check() {
auto my_data = JSONValue([
    JSONValue(1),
    JSONValue(2),
    JSONValue(3),
]);
my_data = JSONValue([
    JSONValue(1),
    JSONValue(2),
    JSONValue(3),
]);
}
