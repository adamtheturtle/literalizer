import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(long.min),
    JSONValue(-0x1),
    JSONValue(0x7fffffffffffffff),
]);
}
