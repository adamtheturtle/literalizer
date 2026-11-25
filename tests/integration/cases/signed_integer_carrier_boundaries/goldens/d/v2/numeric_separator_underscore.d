import std.json;
void main() {
auto my_data = JSONValue([
    "i32_below": JSONValue(-2_147_483_649),
    "i32_minimum": JSONValue(-2_147_483_648),
    "i32_above": JSONValue(-2_147_483_647),
    "i32_maximum": JSONValue(2_147_483_647),
    "i32_over": JSONValue(2_147_483_648),
    "i64_minimum": JSONValue(long.min),
    "i64_maximum": JSONValue(9_223_372_036_854_775_807),
]);
}
