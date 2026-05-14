import std.json;
void main() {
auto my_data = JSONValue([
    // before apple
    JSONValue("apple"),
    JSONValue("banana"),  // banana inline
    // trailing
]);
}
