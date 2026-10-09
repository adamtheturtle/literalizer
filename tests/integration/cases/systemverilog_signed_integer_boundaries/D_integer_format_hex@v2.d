import std.json;
void main() {
auto my_data = JSONValue([
    "i32_below": JSONValue(-0x80000001L),
    "i32_minimum": JSONValue(-0x80000000L),
    "i32_above": JSONValue(-0x7fffffff),
    "i32_maximum": JSONValue(0x7fffffff),
    "i32_over": JSONValue(0x80000000),
    "i64_minimum": JSONValue(long.min),
    "i64_maximum": JSONValue(0x7fffffffffffffff),
]);
}
