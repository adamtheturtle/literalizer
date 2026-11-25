import std.json;
void main() {
auto my_data = JSONValue([
    "flow": JSONValue([
        JSONValue(1),
        // After the first element.
        JSONValue(2),
    ]),
    // Between the key and its value.
    "gap": JSONValue(3),
    // On the block scalar header.
    "block": JSONValue("Text.\n"),
    "nested": JSONValue([
        JSONValue(1),
        JSONValue(1),
        // On the nested alias.
    ]),
    "anchored": JSONValue(4),
    "alias": JSONValue(4),
    // On the alias.
]);
}
