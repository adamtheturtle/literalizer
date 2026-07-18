import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(9223372036854775807),
    "b": JSONValue(9223372036854775808UL),
]);
}
