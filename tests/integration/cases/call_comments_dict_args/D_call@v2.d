import std.json;
void main() {
int process(T...)(T args) { return 0; }
// Test cases
process(JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_1")]));  // first case
process(JSONValue(["type": JSONValue("update"), "pr_id": JSONValue("pr_2")]));  // second case
// third case
process(JSONValue(["type": JSONValue("delete"), "pr_id": JSONValue("pr_3")]));
}
