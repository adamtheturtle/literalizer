import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("custom base after empty collision: )\"\nvalue"),
    JSONValue("custom suffix after base collision: )\" and )x0\"\nvalue"),
    JSONValue("custom second suffix: )\" and )x0\" and )x00\"\nvalue"),
    JSONValue("long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"),
]);
}
