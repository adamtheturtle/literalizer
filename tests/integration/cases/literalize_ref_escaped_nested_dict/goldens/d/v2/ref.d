import std.json;
void main() {
auto existing = JSONValue(1);
auto my_data = JSONValue([
    "nested": JSONValue([JSONValue(0), existing]),
]);
}
