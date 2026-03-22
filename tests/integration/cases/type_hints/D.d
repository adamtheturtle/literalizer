import std.json;
void _check() {
    auto _v = JSONValue([
    "name": JSONValue("Alice"),
    "age": JSONValue(30),
    "active": JSONValue(true),
    "score": JSONValue(null),
]);
}
