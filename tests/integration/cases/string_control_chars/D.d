import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue("line1\nline2"),
    JSONValue("line1line2"),
    JSONValue(""),
]);
}
