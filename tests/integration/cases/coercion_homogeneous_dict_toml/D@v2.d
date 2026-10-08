import std.json;
void main() {
auto my_data = JSONValue([
    "_": JSONValue(["a": JSONValue(1), "b": JSONValue(2)]),
]);
}
