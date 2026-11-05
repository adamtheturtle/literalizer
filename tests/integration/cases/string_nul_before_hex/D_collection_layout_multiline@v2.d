import std.json;
void main() {
auto my_data = JSONValue([
    "x": JSONValue("before\x00after"),
]);
}
