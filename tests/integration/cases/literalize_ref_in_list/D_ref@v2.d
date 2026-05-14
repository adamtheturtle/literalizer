import std.json;
void main() {
auto val_x = JSONValue([
    "_": JSONValue("_"),
]);
auto val_y = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    val_x,
    val_y,
]);
}
