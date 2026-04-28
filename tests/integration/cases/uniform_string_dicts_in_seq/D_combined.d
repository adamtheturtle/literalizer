import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["first": JSONValue("Alice"), "last": JSONValue("Smith")]),
    JSONValue(["first": JSONValue("Bob"), "last": JSONValue("Jones")]),
]);
my_data = JSONValue([
    JSONValue(["first": JSONValue("Alice"), "last": JSONValue("Smith")]),
    JSONValue(["first": JSONValue("Bob"), "last": JSONValue("Jones")]),
]);
}
