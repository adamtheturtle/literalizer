import std.json;
void main() {
auto my_data = JSONValue([
    // outer heading
    // first empty
    "a": parseJSON("{}"),
    // second empty
    "b": parseJSON("{}"),
]);
}
