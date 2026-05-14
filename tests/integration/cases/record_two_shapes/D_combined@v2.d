import std.json;
void main() {
auto my_data = JSONValue([
    "user": JSONValue(["id": JSONValue(1), "name": JSONValue("Alice")]),
    "project": JSONValue(["title": JSONValue("report"), "tags": JSONValue([JSONValue("draft"), JSONValue("urgent")])]),
]);
my_data = JSONValue([
    "user": JSONValue(["id": JSONValue(1), "name": JSONValue("Alice")]),
    "project": JSONValue(["title": JSONValue("report"), "tags": JSONValue([JSONValue("draft"), JSONValue("urgent")])]),
]);
}
