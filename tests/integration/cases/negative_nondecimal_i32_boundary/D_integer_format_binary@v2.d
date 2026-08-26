import std.json;
void main() {
auto my_data = JSONValue([
    "minimum": JSONValue(-0b10000000000000000000000000000000L),
    "below": JSONValue(-0b10110010110100000101111000000000L),
]);
}
