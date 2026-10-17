import std.json;
void main() {
auto my_data = JSONValue([
    "_": JSONValue([JSONValue(1), JSONValue(2.5), JSONValue(3)]),
]);
}
