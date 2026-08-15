import std.json;
void main() {
auto other = JSONValue("true");
auto my_data = JSONValue([
    "main": JSONValue(["x": JSONValue(1), "y": JSONValue("s")]),
]);
}
