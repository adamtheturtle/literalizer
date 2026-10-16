import std.json;
void main() {
auto my_data = JSONValue([
    // outer heading
    // first empty
    parseJSON("[]"),
    // second empty
    parseJSON("[]"),
]);
}
