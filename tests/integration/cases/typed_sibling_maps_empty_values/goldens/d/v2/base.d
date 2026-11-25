import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["m": parseJSON("{}")]),
    JSONValue(["m": parseJSON("{}")]),
]);
}
