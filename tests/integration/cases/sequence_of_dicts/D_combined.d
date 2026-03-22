import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue(["name": JSONValue("Alice"), "age": JSONValue(30)]),
    JSONValue(["name": JSONValue("Bob"), "age": JSONValue(25)]),
]);
my_data = JSONValue([
    JSONValue(["name": JSONValue("Alice"), "age": JSONValue(30)]),
    JSONValue(["name": JSONValue("Bob"), "age": JSONValue(25)]),
]);
}
