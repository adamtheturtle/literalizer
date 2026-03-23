import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue("line1\nline2"),
    JSONValue("line1line2"),
    JSONValue(""),
]);
}
