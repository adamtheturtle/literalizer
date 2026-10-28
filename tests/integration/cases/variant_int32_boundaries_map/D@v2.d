import std.json;
void main() {
auto my_data = JSONValue([
    "below": JSONValue(-2147483649),
    "minimum": JSONValue(-2147483648),
    "above": JSONValue(-2147483647),
    "nested": JSONValue([JSONValue(0)]),
]);
}
