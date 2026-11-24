import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("set_task"), JSONValue("web"), JSONValue("lint_web")]),
    JSONValue([JSONValue("merge_pipelines")]),
]);
}
