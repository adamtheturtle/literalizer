import std.json;
void main() {
auto my_data = JSONValue([
    "below": JSONValue(-0x80000001L),
    "minimum": JSONValue(-0x80000000L),
    "above": JSONValue(-0x7fffffff),
    "nested": JSONValue([JSONValue(0x0)]),
]);
}
