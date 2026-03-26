import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_1"), "draft": JSONValue(true)]),
    JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_2")]),
]);
my_data = JSONValue([
    JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_1"), "draft": JSONValue(true)]),
    JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_2")]),
]);
}
