import std.json;
void main() {
auto deep = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    "a": JSONValue(["b": JSONValue(["c": deep])]),
]);
}
