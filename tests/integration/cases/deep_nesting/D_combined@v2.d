import std.json;
void main() {
auto my_data = JSONValue([
    "level1": JSONValue(["level2": JSONValue(["level3": JSONValue(["level4": JSONValue(["value": JSONValue("deep"), "items": JSONValue([JSONValue("a"), JSONValue("b")])])]), "sibling": JSONValue(42)]), "tags": JSONValue([JSONValue(["name": JSONValue("tag1"), "meta": JSONValue(["priority": JSONValue(1), "labels": JSONValue([JSONValue("x"), JSONValue("y")])])])])]),
]);
my_data = JSONValue([
    "level1": JSONValue(["level2": JSONValue(["level3": JSONValue(["level4": JSONValue(["value": JSONValue("deep"), "items": JSONValue([JSONValue("a"), JSONValue("b")])])]), "sibling": JSONValue(42)]), "tags": JSONValue([JSONValue(["name": JSONValue("tag1"), "meta": JSONValue(["priority": JSONValue(1), "labels": JSONValue([JSONValue("x"), JSONValue("y")])])])])]),
]);
}
