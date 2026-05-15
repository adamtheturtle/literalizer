import std.json;
void main() {
auto shared_var = JSONValue([
    "_": JSONValue("_"),
]);
auto my_data = JSONValue([
    shared_var,
    shared_var,
]);
}
