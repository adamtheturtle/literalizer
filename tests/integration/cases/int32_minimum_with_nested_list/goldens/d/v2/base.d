import std.json;
void main() {
auto my_data = JSONValue([
    "minimum": JSONValue(-2147483648),
    "neighbor": JSONValue(-2147483647),
    "maximum": JSONValue(2147483647),
    "nested": JSONValue([JSONValue(-2147483648)]),
]);
}
