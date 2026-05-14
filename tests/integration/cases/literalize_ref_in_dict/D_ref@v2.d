import std.json;
void main() {
auto my_var = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    "key": my_var,
]);
}
