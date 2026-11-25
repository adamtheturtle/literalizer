import std.json;
void main() {
auto my_data = JSONValue([
    "i32_below": JSONValue(-2147483649),
    "i32_minimum": JSONValue(-2147483648),
    "i32_above": JSONValue(-2147483647),
    "i32_maximum": JSONValue(2147483647),
    "i32_over": JSONValue(2147483648),
    "i64_minimum": JSONValue(long.min),
    "i64_maximum": JSONValue(9223372036854775807),
]);
}
