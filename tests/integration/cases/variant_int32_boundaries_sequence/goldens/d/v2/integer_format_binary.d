import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(-0b10000000000000000000000000000000L),
    JSONValue(-0b1111111111111111111111111111111),
    JSONValue([JSONValue(0b0)]),
]);
}
