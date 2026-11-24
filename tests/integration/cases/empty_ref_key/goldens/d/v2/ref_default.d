import std.json;
void main() {
auto external_value = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    external_value,
]);
}
