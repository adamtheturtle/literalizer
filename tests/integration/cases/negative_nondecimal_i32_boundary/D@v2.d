import std.json;
void main() {
auto my_data = JSONValue([
    "minimum": JSONValue(-2147483648),
    "below": JSONValue(-3000000000),
]);
}
