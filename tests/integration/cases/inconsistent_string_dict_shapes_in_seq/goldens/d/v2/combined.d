import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["first": JSONValue("Alice"), "last": JSONValue("Smith")]),
    JSONValue(["first": JSONValue("Bob"), "middle": JSONValue("Quincy")]),
]);
my_data = JSONValue([
    JSONValue(["first": JSONValue("Alice"), "last": JSONValue("Smith")]),
    JSONValue(["first": JSONValue("Bob"), "middle": JSONValue("Quincy")]),
]);
}
