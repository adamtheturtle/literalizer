import std.json;

void _check() {
    auto _v = JSONValue([
    // before apple
    JSONValue("apple"),
    JSONValue("banana"),  // banana inline
    // trailing
]);
}
