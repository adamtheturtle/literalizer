import std.json;

void _check() {
auto my_data = JSONValue([
    "name": JSONValue("Alice"),
    "score": JSONValue(null),
    "age": JSONValue(30),
]);
}
