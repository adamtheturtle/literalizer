import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(long.min),
    JSONValue(-0b1),
    JSONValue(0b111111111111111111111111111111111111111111111111111111111111111),
]);
}
