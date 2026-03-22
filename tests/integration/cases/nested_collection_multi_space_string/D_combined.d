import std.json;

void _check() {
auto my_data = JSONValue([
    JSONValue(["key": JSONValue("hello   world"), "value": JSONValue(1)]),
]);
my_data = JSONValue([
    JSONValue(["key": JSONValue("hello   world"), "value": JSONValue(1)]),
]);
}
