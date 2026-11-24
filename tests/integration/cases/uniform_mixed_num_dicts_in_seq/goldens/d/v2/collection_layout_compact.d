import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["x": JSONValue(1), "y": JSONValue(2.5)]),
    JSONValue(["x": JSONValue(3), "y": JSONValue(4.0)]),
]);
}
