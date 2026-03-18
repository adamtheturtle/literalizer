import std.json;

void _check() {
auto my_data = JSONValue([
    JSONValue("apple"),  // inline comment
    // before banana
    JSONValue("banana"),
    // trailing
]);
}
