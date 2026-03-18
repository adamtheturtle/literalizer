import std.json;

void _check() {
    auto _v = JSONValue([
    JSONValue(["name": JSONValue("Alice"), "age": JSONValue(30)]),
    JSONValue(["name": JSONValue("Bob"), "age": JSONValue(25)]),
]);
}
