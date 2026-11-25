import std.json;
void main() {
auto my_data = JSONValue([
    "values": JSONValue([JSONValue(1), JSONValue(2147483648)]),
]);
}
