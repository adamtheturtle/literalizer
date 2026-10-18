import std.json;
void main() {
auto my_data = JSONValue([
    "minimum": JSONValue(-0x80000000L),
    "neighbor": JSONValue(-0x7fffffff),
    "maximum": JSONValue(0x7fffffff),
    "nested": JSONValue([JSONValue(-0x80000000L)]),
]);
}
