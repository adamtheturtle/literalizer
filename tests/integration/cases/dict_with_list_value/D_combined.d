import std.json;
void _check() {
auto my_data = JSONValue([
    "name": JSONValue("Alice"),
    "scores": JSONValue([JSONValue(10), JSONValue(20), JSONValue(30)]),
]);
my_data = JSONValue([
    "name": JSONValue("Alice"),
    "scores": JSONValue([JSONValue(10), JSONValue(20), JSONValue(30)]),
]);
}
