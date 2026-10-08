import std.json;
void main() {
auto string_map = JSONValue([
    "k": JSONValue("s"),
]);
auto my_data = JSONValue([
    string_map,
    JSONValue(["k": JSONValue(1)]),
]);
}
