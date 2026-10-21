import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(0x1),
    "b": JSONValue(0x10000000000),
]);
}
