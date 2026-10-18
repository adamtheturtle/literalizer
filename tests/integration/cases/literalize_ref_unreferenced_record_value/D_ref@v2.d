import std.json;
void main() {
auto my_data = JSONValue([
    "main": JSONValue(["x": JSONValue(1), "y": JSONValue("s")]),
]);
}
