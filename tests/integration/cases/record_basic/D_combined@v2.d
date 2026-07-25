import std.json;
void main() {
auto my_data = JSONValue([
    "id": JSONValue(1),
    "label": JSONValue("She said \"hello\", then waved"),
    "enabled": JSONValue(false),
    "related_ids": JSONValue([JSONValue(1), JSONValue(2), JSONValue(3)]),
]);
my_data = JSONValue([
    "id": JSONValue(1),
    "label": JSONValue("She said \"hello\", then waved"),
    "enabled": JSONValue(false),
    "related_ids": JSONValue([JSONValue(1), JSONValue(2), JSONValue(3)]),
]);
}
