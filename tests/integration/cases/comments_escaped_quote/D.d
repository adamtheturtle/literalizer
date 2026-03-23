import std.json;
void _check() {
    auto _v = JSONValue([
    "key": JSONValue("value \" # not a comment"),  // real
]);
}
