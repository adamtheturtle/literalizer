import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([
        JSONValue(["item": JSONValue("existing")]),
        JSONValue("kept"),
        // This comment trails the first pair.
    ]),
    JSONValue([JSONValue(["item": JSONValue("next")]), JSONValue("also kept")]),
    // This comment describes the last pair.
    JSONValue([JSONValue(["item": JSONValue("last")]), JSONValue("kept too")]),
]);
}
