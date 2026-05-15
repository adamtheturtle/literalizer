import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["id": JSONValue(1), "label": JSONValue("first"), "tags": parseJSON("[]")]),
    JSONValue(["id": JSONValue(2), "label": JSONValue("second"), "tags": parseJSON("[]")]),
    JSONValue(["id": JSONValue(3), "label": JSONValue("third"), "tags": parseJSON("[]")]),
]);
my_data = JSONValue([
    JSONValue(["id": JSONValue(1), "label": JSONValue("first"), "tags": parseJSON("[]")]),
    JSONValue(["id": JSONValue(2), "label": JSONValue("second"), "tags": parseJSON("[]")]),
    JSONValue(["id": JSONValue(3), "label": JSONValue("third"), "tags": parseJSON("[]")]),
]);
}
