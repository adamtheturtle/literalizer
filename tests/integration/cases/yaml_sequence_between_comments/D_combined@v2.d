import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["item": JSONValue("existing")]),
    // This comment describes the next item.
    JSONValue(["item": JSONValue("next")]),
]);
my_data = JSONValue([
    JSONValue(["item": JSONValue("existing")]),
    // This comment describes the next item.
    JSONValue(["item": JSONValue("next")]),
]);
}
