import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue("line1\r\nline2"),
    JSONValue("line1\rline2"),
    JSONValue(""),
]);
}
