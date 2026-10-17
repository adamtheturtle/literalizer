import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(long.min),
    JSONValue(0b1000000000000000000000000000000000000000000000000000000000000000UL),
]);
}
