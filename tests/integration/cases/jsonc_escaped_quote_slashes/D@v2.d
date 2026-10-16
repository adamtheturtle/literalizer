import std.json;
void main() {
auto my_data = JSONValue([
    "text": JSONValue("a\"//b"),
]);
}
