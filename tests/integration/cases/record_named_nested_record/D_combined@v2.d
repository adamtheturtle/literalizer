import std.json;
void main() {
auto my_data = JSONValue([
    "project": JSONValue("alpha"),
    "lead_item": JSONValue(["id": JSONValue(100), "label": JSONValue("first item"), "enabled": JSONValue(false), "related_ids": JSONValue([JSONValue(102), JSONValue(103)])]),
]);
my_data = JSONValue([
    "project": JSONValue("alpha"),
    "lead_item": JSONValue(["id": JSONValue(100), "label": JSONValue("first item"), "enabled": JSONValue(false), "related_ids": JSONValue([JSONValue(102), JSONValue(103)])]),
]);
}
