import std.json;
void main() {
auto my_data = JSONValue([
    "v": JSONValue("a\u202A\x00é😀b"),
]);
}
