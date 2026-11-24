import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["name": JSONValue("Alice"), "age": JSONValue(30)]),
    JSONValue(["name": JSONValue("Bob"), "age": JSONValue(25)]),
]);
}
