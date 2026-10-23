import std.json;
void main() {
auto my_data = JSONValue([
    parseJSON("{}"),
    parseJSON("[]"),
]);
}
