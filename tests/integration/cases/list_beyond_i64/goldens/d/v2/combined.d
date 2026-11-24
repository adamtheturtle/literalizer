import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(9223372036854775807),
    JSONValue(9223372036854775808UL),
]);
my_data = JSONValue([
    JSONValue(9223372036854775807),
    JSONValue(9223372036854775808UL),
]);
}
