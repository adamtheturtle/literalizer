import std.json;
void main() {
auto my_data = JSONValue([
    "id": JSONValue(1),
    "description": JSONValue("She said \"hello\", then waved"),
    "is_done": JSONValue(false),
    "blocks": JSONValue([JSONValue(1), JSONValue(2), JSONValue(3)]),
]);
}
