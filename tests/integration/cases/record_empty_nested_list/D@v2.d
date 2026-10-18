import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue([JSONValue(1), JSONValue(2)]), JSONValue([JSONValue(3)])]),
    "b": JSONValue([parseJSON("[]"), JSONValue([JSONValue(1)])]),
]);
}
