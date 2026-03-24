import std.json;
void _check() {
    auto my_data = JSONValue([
    JSONValue("line1\r\nline2"),
    JSONValue("line1\rline2"),
    JSONValue(""),
]);
}
