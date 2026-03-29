import std.json;
void _check() {
auto my_data = JSONValue([
    "1": JSONValue("one"),
    "2": JSONValue("two"),
    "42": JSONValue("answer"),
]);
}
