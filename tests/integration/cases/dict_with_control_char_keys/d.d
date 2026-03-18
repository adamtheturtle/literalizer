import std.json;

void _check() {
    auto _v = JSONValue([
    "key\nwith\nnewlines": JSONValue("value1"),
    "key	with	tabs": JSONValue("value2"),
]);
}
