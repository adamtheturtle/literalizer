import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue([JSONValue(1), JSONValue(2)])]),
    "b": JSONValue([JSONValue([JSONValue(3)])]),
]);
}
