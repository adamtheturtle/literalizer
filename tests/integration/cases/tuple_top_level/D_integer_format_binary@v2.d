import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(0b1),
    JSONValue("email"),
    JSONValue("a@gmail.com"),
    JSONValue(0b1100100),
]);
}
