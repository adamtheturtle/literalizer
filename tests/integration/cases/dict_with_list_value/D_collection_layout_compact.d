import std.json;
void main() {
auto my_data = JSONValue([
    "name": JSONValue("Alice"),
    "scores": JSONValue([JSONValue(10), JSONValue(20), JSONValue(30)]),
]);
}
