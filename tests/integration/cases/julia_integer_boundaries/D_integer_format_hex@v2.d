import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(long.min),
    JSONValue(0x8000000000000000UL),
]);
}
