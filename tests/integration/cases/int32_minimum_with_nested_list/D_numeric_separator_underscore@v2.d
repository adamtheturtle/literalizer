import std.json;
void main() {
auto my_data = JSONValue([
    "minimum": JSONValue(-2_147_483_648),
    "neighbor": JSONValue(-2_147_483_647),
    "maximum": JSONValue(2_147_483_647),
    "nested": JSONValue([JSONValue(-2_147_483_648)]),
]);
}
