import std.json;
void main() {
struct MgrType_ { int op(T...)(T args) { return 0; } }
struct AppType_ { MgrType_ mgr; }
AppType_ app;
app.mgr.op(JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_1"), "draft": JSONValue(true)]));
app.mgr.op(JSONValue(["type": JSONValue("create"), "pr_id": JSONValue("pr_2")]));
}
