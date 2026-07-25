import std.json;
void main() {
auto my_data = JSONValue([
    "collection": JSONValue("alpha"),
    "featured_entry": JSONValue(["id": JSONValue(100), "label": JSONValue("first entry"), "enabled": JSONValue(false), "related_ids": JSONValue([JSONValue(102), JSONValue(103)])]),
]);
my_data = JSONValue([
    "collection": JSONValue("alpha"),
    "featured_entry": JSONValue(["id": JSONValue(100), "label": JSONValue("first entry"), "enabled": JSONValue(false), "related_ids": JSONValue([JSONValue(102), JSONValue(103)])]),
]);
}
