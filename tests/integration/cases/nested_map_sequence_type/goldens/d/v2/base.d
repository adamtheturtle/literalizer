import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(["b": JSONValue([JSONValue(1), JSONValue(2), JSONValue(3)])]),
]);
}
