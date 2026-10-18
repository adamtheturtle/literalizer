import std.json;
void main() {
auto sibling_map = JSONValue([
    "k": JSONValue(2),
]);
auto my_data = JSONValue([
    JSONValue(["k": JSONValue(1)]),
    sibling_map,
]);
}
