import std.json;
void main() {
auto my_data = JSONValue([
    "minimum": JSONValue(-2_147_483_648),
    "below": JSONValue(-3_000_000_000),
]);
}
