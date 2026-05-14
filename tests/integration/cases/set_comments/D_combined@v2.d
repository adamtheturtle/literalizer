import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("apple"),  // inline comment
    // before banana
    JSONValue("banana"),
    // trailing
]);
my_data = JSONValue([
    JSONValue("apple"),  // inline comment
    // before banana
    JSONValue("banana"),
    // trailing
]);
}
