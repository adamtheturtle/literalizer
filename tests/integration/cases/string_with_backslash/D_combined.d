import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue("C:\\path\\to\\file"),
    JSONValue("back\\\\slash"),
    JSONValue("hello \\\"world\\\""),
]);
my_data = JSONValue([
    JSONValue("C:\\path\\to\\file"),
    JSONValue("back\\\\slash"),
    JSONValue("hello \\\"world\\\""),
]);
}
