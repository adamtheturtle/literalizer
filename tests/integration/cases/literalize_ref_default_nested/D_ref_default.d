import std.json;
void main() {
auto item_var = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    "items": JSONValue([item_var, JSONValue(["fallback": JSONValue("value")])]),
]);
}
