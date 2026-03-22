import std.json;
void _check() {
    auto _v = JSONValue([
    "key\nwith\nnewlines": JSONValue("value1"),
    "key\twith\ttabs": JSONValue("value2"),
    "": JSONValue("value3"),
]);
}
