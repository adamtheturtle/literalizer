import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["id": JSONValue(100), "label": JSONValue("first item"), "enabled": JSONValue(false), "related_ids": JSONValue([JSONValue(102), JSONValue(103)])]),
    JSONValue(["id": JSONValue(101), "label": JSONValue("second item"), "enabled": JSONValue(true), "related_ids": JSONValue([JSONValue(100)])]),
]);
}
