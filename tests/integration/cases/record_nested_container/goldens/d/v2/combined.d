import std.json;
void main() {
auto my_data = JSONValue([
    "title": JSONValue("report"),
    "tags": JSONValue([JSONValue("draft"), JSONValue("urgent"), JSONValue("review")]),
    "priority": JSONValue(2),
]);
my_data = JSONValue([
    "title": JSONValue("report"),
    "tags": JSONValue([JSONValue("draft"), JSONValue("urgent"), JSONValue("review")]),
    "priority": JSONValue(2),
]);
}
