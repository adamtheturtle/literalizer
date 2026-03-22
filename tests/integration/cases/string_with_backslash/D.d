import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue("C:\\path\\to\\file"),
    JSONValue("back\\\\slash"),
    JSONValue("hello \\\"world\\\""),
]);
}
