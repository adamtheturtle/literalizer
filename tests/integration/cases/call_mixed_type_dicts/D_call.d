import std.json;
void _check() {
struct MType_ { int Op(T...)(T args) { return 0; } }
MType_ m;
m.Op(JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_1"), "draft": JSONValue(true)]));
m.Op(JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_2")]));
}
