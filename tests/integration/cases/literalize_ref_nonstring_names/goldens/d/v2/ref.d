import std.json;
void main() {
auto actual = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    JSONValue(["$ref": JSONValue(1)]),
    JSONValue(["$ref": JSONValue(null)]),
    actual,
]);
}
