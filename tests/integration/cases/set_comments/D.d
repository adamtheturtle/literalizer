import std.json;
void _check() {
    auto _v = JSONValue([
    JSONValue("apple"),  // inline comment
    // before banana
    JSONValue("banana"),
    // trailing
]);
}
