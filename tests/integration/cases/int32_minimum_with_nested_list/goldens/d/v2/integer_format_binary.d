import std.json;
void main() {
auto my_data = JSONValue([
    "minimum": JSONValue(-0b10000000000000000000000000000000L),
    "neighbor": JSONValue(-0b1111111111111111111111111111111),
    "maximum": JSONValue(0b1111111111111111111111111111111),
    "nested": JSONValue([JSONValue(-0b10000000000000000000000000000000L)]),
]);
}
