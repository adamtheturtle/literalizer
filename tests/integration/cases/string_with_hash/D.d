import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue("issue #{42}"),
    JSONValue("color #red"),
]);
}
