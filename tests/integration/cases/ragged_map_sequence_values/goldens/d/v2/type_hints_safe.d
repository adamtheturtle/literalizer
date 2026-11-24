import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue(["item": JSONValue([JSONValue(1)])])]),
    "b": JSONValue([JSONValue(["item": JSONValue([JSONValue(2), JSONValue(3)])])]),
]);
}
