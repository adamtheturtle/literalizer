import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("first"), JSONValue(["x": JSONValue(1)])]),
    JSONValue([JSONValue("second"), JSONValue(["y": JSONValue(2)])]),
]);
}
