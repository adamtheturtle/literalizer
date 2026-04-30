import std.json;
void main() {
auto x = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    x,
    JSONValue(1),
    JSONValue(2),
]);
}
