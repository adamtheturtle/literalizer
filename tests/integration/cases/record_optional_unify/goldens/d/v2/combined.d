import std.json;
void main() {
auto my_data = JSONValue([
    "items": JSONValue([JSONValue(["id": JSONValue(1)]), JSONValue(["id": JSONValue(2), "count": JSONValue(10)]), JSONValue(["id": JSONValue(3), "count": JSONValue(20)])]),
]);
my_data = JSONValue([
    "items": JSONValue([JSONValue(["id": JSONValue(1)]), JSONValue(["id": JSONValue(2), "count": JSONValue(10)]), JSONValue(["id": JSONValue(3), "count": JSONValue(20)])]),
]);
}
