import std.json;
void main() {
auto my_data = JSONValue([
    "id": JSONValue(1),
    "owner": JSONValue(["name": JSONValue("Alice"), "age": JSONValue(30)]),
]);
}
