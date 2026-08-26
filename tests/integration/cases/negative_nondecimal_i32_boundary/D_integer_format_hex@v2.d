import std.json;
void main() {
auto my_data = JSONValue([
    "minimum": JSONValue(-0x80000000L),
    "below": JSONValue(-0xb2d05e00L),
]);
}
