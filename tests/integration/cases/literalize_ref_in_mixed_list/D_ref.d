import std.json;
void main() {
auto ref_x = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    ref_x,
    JSONValue(1),
    JSONValue(2),
]);
}
