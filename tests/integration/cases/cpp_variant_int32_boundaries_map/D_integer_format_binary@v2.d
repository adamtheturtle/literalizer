import std.json;
void main() {
auto my_data = JSONValue([
    "below": JSONValue(-0b10000000000000000000000000000001L),
    "minimum": JSONValue(-0b10000000000000000000000000000000L),
    "above": JSONValue(-0b1111111111111111111111111111111),
    "nested": JSONValue([JSONValue(0b0)]),
]);
}
