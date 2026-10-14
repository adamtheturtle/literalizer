import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(-0x80000000L),
    JSONValue(-0x7fffffff),
    JSONValue([JSONValue(0x0)]),
]);
}
