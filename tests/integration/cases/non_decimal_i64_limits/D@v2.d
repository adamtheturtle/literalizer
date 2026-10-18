import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(long.min),
    JSONValue(-1),
    JSONValue(9223372036854775807),
]);
}
