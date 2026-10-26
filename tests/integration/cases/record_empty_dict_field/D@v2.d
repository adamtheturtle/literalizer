import std.json;
void main() {
auto my_data = JSONValue([
    "f": parseJSON("{}"),
    "g": JSONValue(1),
]);
}
