import std.json;
void _check() {
struct MgrType_ { int Op(T...)(T args) { return 0; } }
MgrType_ mgr;
mgr.Op(JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_1"), "draft": JSONValue(true)]));
mgr.Op(JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_2")]));
}
