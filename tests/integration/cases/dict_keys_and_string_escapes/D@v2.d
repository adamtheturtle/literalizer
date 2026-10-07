import std.json;
void main() {
auto my_data = JSONValue([
    "plain": JSONValue([JSONValue(1), JSONValue(2)]),
    "with-dash": JSONValue("a\nb"),
]);
}
