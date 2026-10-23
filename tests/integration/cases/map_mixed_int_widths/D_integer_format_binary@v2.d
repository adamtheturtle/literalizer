import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(0b1),
    "b": JSONValue(0b10000000000000000000000000000000000000000),
]);
}
