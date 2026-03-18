import std.json;

void _check() {
    auto _v = JSONValue([
    parseJSON("[]"),
    parseJSON("{}"),
]);
}
