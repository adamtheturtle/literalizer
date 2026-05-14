import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["id": JSONValue(1), "label": JSONValue("first")]),
    JSONValue(["id": JSONValue(2), "label": JSONValue("second")]),
    JSONValue(["id": JSONValue(3), "label": JSONValue("third")]),
]);
}
