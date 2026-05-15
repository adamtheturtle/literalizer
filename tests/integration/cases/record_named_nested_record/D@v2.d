import std.json;
void main() {
auto my_data = JSONValue([
    "project": JSONValue("alpha"),
    "lead_task": JSONValue(["id": JSONValue(100), "description": JSONValue("first task"), "is_done": JSONValue(false), "blocks": JSONValue([JSONValue(102), JSONValue(103)])]),
]);
}
