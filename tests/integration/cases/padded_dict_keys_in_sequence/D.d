import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue(["first": JSONValue("Alice"), "last": JSONValue("Smith"), "middle": JSONValue("Jane")]),
    JSONValue(["first": JSONValue("Bob"), "last": JSONValue("Jones")]),
]);
}
