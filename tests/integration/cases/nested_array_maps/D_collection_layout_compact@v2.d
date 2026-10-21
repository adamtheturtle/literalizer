import std.json;
void main() {
auto my_data = JSONValue([
    "groups": JSONValue([JSONValue([JSONValue(["id": JSONValue(1)])]), JSONValue([JSONValue(["id": JSONValue(2)])])]),
]);
}
