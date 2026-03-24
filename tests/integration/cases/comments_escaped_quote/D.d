import std.json;
void _check() {
    auto my_data = JSONValue([
    "key": JSONValue("value \" # not a comment"),  // real
]);
}
