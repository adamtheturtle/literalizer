import std.json;
void main() {
auto my_data = JSONValue([
    "first": JSONValue(["items": JSONValue([JSONValue(1), JSONValue(["value": JSONValue(2)])])]),
    "second": JSONValue(["items": JSONValue([JSONValue(1), JSONValue(["value": JSONValue(3)])])]),
]);
}
