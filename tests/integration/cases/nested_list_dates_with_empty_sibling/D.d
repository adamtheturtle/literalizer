import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue([JSONValue("2026-01-01"), JSONValue("2026-01-02")]),
    parseJSON("[]"),
    JSONValue([JSONValue("2026-02-03"), JSONValue("2026-02-04")]),
]);
}
