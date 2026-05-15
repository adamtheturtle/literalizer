import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["id": JSONValue(100), "description": JSONValue("first task"), "is_done": JSONValue(false), "blocks": JSONValue([JSONValue(102), JSONValue(103)])]),
    JSONValue(["id": JSONValue(101), "description": JSONValue("second task"), "is_done": JSONValue(true), "blocks": parseJSON("[]")]),
]);
my_data = JSONValue([
    JSONValue(["id": JSONValue(100), "description": JSONValue("first task"), "is_done": JSONValue(false), "blocks": JSONValue([JSONValue(102), JSONValue(103)])]),
    JSONValue(["id": JSONValue(101), "description": JSONValue("second task"), "is_done": JSONValue(true), "blocks": parseJSON("[]")]),
]);
}
