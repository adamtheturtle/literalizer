import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(0x7fffffffffffffff),
    "b": JSONValue(0x8000000000000000UL),
]);
}
