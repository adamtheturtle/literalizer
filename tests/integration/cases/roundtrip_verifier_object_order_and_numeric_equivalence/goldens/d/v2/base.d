import std.json;
void main() {
auto my_data = JSONValue([
    "b": JSONValue(null),
    "a": JSONValue(["y": JSONValue([JSONValue(1.0)]), "x": JSONValue(false)]),
]);
}
