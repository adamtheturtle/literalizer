import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("a b c"),
    JSONValue("a\r b"),
]);
}
