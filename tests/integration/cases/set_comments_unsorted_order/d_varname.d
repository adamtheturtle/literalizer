import std.json;

void _check() {
auto my_data = JSONValue([
    // before apple
    JSONValue("apple"),
    JSONValue("banana"),  // banana inline
    // trailing
]);
}
