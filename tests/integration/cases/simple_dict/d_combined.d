import std.json;

void _check() {
auto my_data = JSONValue([
    "name": JSONValue("Alice"),
    "age": JSONValue(30),
    "active": JSONValue(true),
    "score": JSONValue(null),
]);
my_data = JSONValue([
    "name": JSONValue("Alice"),
    "age": JSONValue(30),
    "active": JSONValue(true),
    "score": JSONValue(null),
]);
}
