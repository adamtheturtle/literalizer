import std.json;
void main() {
auto my_data = JSONValue([
    "first": JSONValue(["x": JSONValue(1), "y": JSONValue(2)]),
    "second": JSONValue(["z": JSONValue(3)]),
]);
}
