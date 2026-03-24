import std.json;
void _check() {
    auto _v = JSONValue([
    "key": JSONValue("\"bang!\""),  // real
]);
}
